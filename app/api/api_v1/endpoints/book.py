from fastapi import APIRouter
from typing import List
from pymongo.errors import DuplicateKeyError 

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
    return opnions




