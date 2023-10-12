from fastapi import APIRouter
from typing import List
from pymongo.errors import DuplicateKeyError 

from app.documents.books.book import BookItem
from app.services.google_books import GoogleBooksService

book_router = APIRouter()

@book_router.get("/category", status_code=200)
async def retrieve_books_by_category(category: str) -> List[BookItem]:
    books = await BookItem.find({"volumeInfo.categories": category}).to_list()
    return books

@book_router.get("/", status_code=200)
async def retrieve_books(q: str) -> List[BookItem]:
    google_books = GoogleBooksService()
    books = google_books.retrieve_books(q=q)
    documents = [BookItem(**bk) for bk in books["items"]]
    for doc in documents:
        try:
            await doc.insert()
        except DuplicateKeyError as e:
            continue
    
    return books





