import random
from fastapi import APIRouter

from app.documents.books.book import BookItem

suggestion_router = APIRouter()

@suggestion_router.get("/", status_code=200)
async def retrieve_suggestion() -> BookItem:
    books = await BookItem.find({"volumeInfo.imageLinks.thumbnail": {"$exists": True}}).to_list()
    indices_aleatorios = random.sample(range(len(books)), 60)
    livros_selecionados = [books[i] for i in indices_aleatorios]
    return livros_selecionados





