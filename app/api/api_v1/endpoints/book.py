

import nltk
import numpy as np
import tflite_runtime.interpreter as tflite

import re
import string

from fastapi import APIRouter
from typing import List
from pymongo.errors import DuplicateKeyError 
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


from app.documents.books.book import BookItem, Opinion
from app.services.google_books import GoogleBooksService

book_router = APIRouter()

nltk.download('punkt')
nltk.download('stopwords')

@book_router.get("/", status_code=200)
async def retrieve_books(q: str= "", s: str = "") -> List[BookItem]:
    google_books = GoogleBooksService()
    books = google_books.retrieve_books(q=q, s=s)
    if books["totalItems"] > 0:
        documents = [
            BookItem(**bk) 
            for bk in books["items"] 
            if bk["volumeInfo"].get("imageLinks")
        ]
        for doc in documents:
            try:
                await doc.insert()
            except DuplicateKeyError as e:
                continue
        
        return documents

    return []

@book_router.get("/{book_id}", status_code=200)
async def retrieve_books(book_id: str) -> BookItem:
    book = await BookItem.get(book_id)    
    return book


def encode_words(words, vocab):
    # Mapeie palavras para índices usando uma tabela de vocabulário
    indices = [vocab.get(word, 0) for word in words]
    return indices

@book_router.get("/opinion/{book_id}", status_code=200)
async def retrieve_opnions_by_books(book_id: str) -> List[Opinion] :
    opnions = await Opinion.find({"book_id": book_id}).to_list()
    vocab = {word: idx + 1 for idx, word in enumerate(set(string.punctuation))}
    interpreter = False
    for opnion in opnions:
        
        # if opnion.classification:
        #     continue
        
        tflite_path = './app/model/modelo.tflite'
        interpreter = tflite.Interpreter(model_path=tflite_path)
        
        interpreter.allocate_tensors()
        # Obtenha os tensores de entrada e saída
        input_tensor_index = interpreter.get_input_details()[0]['index']
        output = interpreter.tensor(interpreter.get_output_details()[0]['index'])
    
        text = opnion.text
        text = clean_text(text)
        
        vocab = {word: idx + 1 for idx, word in enumerate(set(text))}
        text_encoded = encode_words(text, vocab)
        
        # Ajuste a sequência para o tamanho esperado pelo modelo
        sequence_length = 1120
        if len(text_encoded) < sequence_length:
            # Se a sequência for menor que o esperado, preencha com zeros à direita
            text_encoded += [0] * (sequence_length - len(text_encoded))
        elif len(text_encoded) > sequence_length:
            # Se a sequência for maior que o esperado, trunque
            text_encoded = text_encoded[:sequence_length]
        
        input_data = np.array([text_encoded], dtype=np.int32)

        # Defina os dados de entrada no tensor do modelo
        interpreter.set_tensor(input_tensor_index, input_data)

        # Execute a inferência
        interpreter.invoke()

        # Obtenha os resultados da inferência
        predictions = output()[0]

        opnion.predict = predictions[0] * 100
        if opnion.predict >= 70:
            classification = "Positivo"
        elif opnion.predict <= 40:
            classification = "Negativo"
        else:
            classification = "Neutro"
            
        
        atualizacao = {
            "$set": {
                "predict": opnion.predict,
                "classification": classification,
            }
        }
        await opnion.update(atualizacao)
        
    del interpreter        
    return opnions


@book_router.post("/opinion", status_code=201)
async def create_user(opnion: Opinion):
    await opnion.create()
    return {"message": "Opnion has been saved"}


def clean_text(text):
    text = BeautifulSoup(text, 'lxml').get_text()
    
    text = re.sub(r'@', ' ', text)
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = text.replace("htt", "").replace("\n", "")
    text = re.sub(r' +', ' ', text)
    
    # Tokenização usando nltk
    words = word_tokenize(text)

    # Remova stop words (opcional)
    stop_words = set(stopwords.words('portuguese'))
    words = [word for word in words if word.lower() not in stop_words and word not in string.punctuation]


    return words


    



