from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from datetime import datetime, timedelta

from app import schemas
from app.core import security
from app.core.config import settings
from app.documents.users.user import UsersDocument, UserCreateDocument

from typing import List
from beanie import PydanticObjectId
from bson import ObjectId

login_router = APIRouter()

@login_router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
    loginData: schemas.Login
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = await UsersDocument.find_one({"nm_email": loginData.username})    
    if not user or not security.verify_password(loginData.password, user.nm_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }