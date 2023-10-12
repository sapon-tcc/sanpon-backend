from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, book, suggestion, categories

api_router = APIRouter()
api_router.include_router(login.login_router, tags=["login"])
api_router.include_router(users.user_router, prefix="/users", tags=["users"])
api_router.include_router(book.book_router, prefix="/books", tags=["books"])
api_router.include_router(suggestion.suggestion_router, prefix="/suggestion", tags=["suggestion"])
api_router.include_router(categories.categories_router, prefix="/categories", tags=["categories"])