from fastapi import APIRouter
from typing import List
from pymongo.errors import DuplicateKeyError 

from app.documents.books.book import BookItem
from app.services.google_books import GoogleBooksService

book_router = APIRouter()



@book_router.get("/", status_code=200)
async def retrieve_books(q: str, s: str) -> List[BookItem]:
    google_books = GoogleBooksService()
    books = google_books.retrieve_books(q=q, s=s)
    if books:
        documents = [
            BookItem(**bk) 
            for bk in books["items"] 
            if bk["volumeInfo"].get("imageLinks")
            and q in bk["volumeInfo"]["title"]
        ]
        for doc in documents:
            try:
                await doc.insert()
            except DuplicateKeyError as e:
                continue
        
        return documents






