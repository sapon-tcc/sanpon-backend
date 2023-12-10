
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds

import spacy as sp
import re
import string

from fastapi import APIRouter
from typing import List
from pymongo.errors import DuplicateKeyError 
from bs4 import BeautifulSoup


from app.documents.books.book import BookItem, Opinion
from app.services.google_books import GoogleBooksService

book_router = APIRouter()



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

@book_router.get("/opinion/{book_id}", status_code=200)
async def retrieve_opnions_by_books(book_id: str) -> List[Opinion] :
    opnions = await Opinion.find({"book_id": book_id}).to_list()
    interpreter = False
    opnions_to_update = []
    for opnion in opnions:
        
        if opnion.predict:
            if not opnion.classification:
                opnions_to_update.append(opnion)
            
            continue
        
        tflite_path = './app/model/modelo.tflite'
        interpreter = tf.lite.Interpreter(model_path=tflite_path)
        
        interpreter.allocate_tensors()
        # Obtenha os tensores de entrada e saída
        input_tensor_index = interpreter.get_input_details()[0]['index']
        output = interpreter.tensor(interpreter.get_output_details()[0]['index'])
    
        text = opnion.text
        text = clean_tweet2(clean_tweet(text))
        tokenizer = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(text, target_vocab_size = 2**16)
        text_encoded = tokenizer.encode(text)
        
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
        opnions_to_update.append(opnion)

    tf.keras.backend.clear_session()
    del interpreter
    
    
    for opnion in opnions_to_update:
        atualizacao = {
            "$set": {
                "predict": opnion.predict,
                "classification": "Positiva" if opnion.predict >= 0.5 else "Negativa",
            }
        }
        
        await opnion.update(atualizacao)
    
    
    return opnions


def clean_tweet(tweet):
    tweet = BeautifulSoup(tweet, 'lxml').get_text()
    
    tweet = re.sub(r'@', ' ', tweet)
    tweet = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', tweet)
    tweet = re.sub(r'\d+', ' ', tweet)
    tweet = tweet.replace("htt", "").replace("\n", "")
    tweet = re.sub(r' +', ' ', tweet)
    
    return tweet

def clean_tweet2(tweet):
    tweet = tweet.lower()
    nlp = sp.load("pt_core_news_sm")
    stop_words = sp.lang.pt.STOP_WORDS
    document = nlp(tweet)
    
    words = []
    for token in document:
        words.append(token.text)
    
    words = [word for word in words if word not in stop_words and word not in string.punctuation]
    words = ' '.join([str(element) for element in words])
    return words



