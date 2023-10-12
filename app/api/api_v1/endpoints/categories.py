from fastapi import APIRouter
from typing import List

from app.documents.books.book import BookItem

categories_router = APIRouter()

@categories_router.get("/", status_code=200)
async def retrieve_categories() -> List[str]:
    books = await BookItem.find_all(limit=1000).to_list()
    
    categories = []
    for book in books:
        if book.volumeInfo.categories:
            categories.extend(book.volumeInfo.categories)
    
    
    return list(set(categories)) 





