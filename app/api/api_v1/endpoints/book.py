from fastapi import APIRouter

from app.documents.books.book import BookDocument
from app.services.google_books import GoogleBooksService

from typing import List
from beanie import PydanticObjectId
from bson import ObjectId

user_router = APIRouter()

@user_router.get("/", status_code=200)
async def retrieve_books(q: str):
    
    google_books = GoogleBooksService()
    books = await google_books.retrieve_books(q=q)
    return books


@user_router.get("/{user_id}", status_code=200)
async def retrieve_book(book_id: PydanticObjectId) -> BookDocument:
    user = await BookDocument.get(book_id)
    return user



