import random
from fastapi import APIRouter

from app.documents.books.book import BookItem

suggestion_router = APIRouter()

@suggestion_router.get("/", status_code=200)
async def retrieve_suggestion() -> BookItem:
    books = await BookItem.find({"volumeInfo.imageLinks.thumbnail": {"$exists": True}}, limit=60).to_list()
    random.shuffle(books)
    return books[:30]





