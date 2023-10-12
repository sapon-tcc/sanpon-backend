from fastapi import APIRouter

from app.documents.books.book import BookItem

suggestion_router = APIRouter()

@suggestion_router.get("/", status_code=200)
async def retrieve_suggestion() -> BookItem:
    return await BookItem.find_all(limit=1000).to_list()





