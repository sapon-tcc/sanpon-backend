from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError 

from app import schemas
from app.documents.users import user
from app.core.config import settings
from app.core import security

from jose import jwt

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

async def get_current_user(
    token: str = Depends(reusable_oauth2)
) -> user.UsersDocument:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    current_user = await user.UsersDocument.get(token_data.sub)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user

async def get_current_active_user(
    current_user: user.UsersDocument = Depends(get_current_user),
) -> user.UsersDocument:
    return current_user

async def get_current_active_superuser(
    current_user: user.UsersDocument = Depends(get_current_user),
) -> user.UsersDocument:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user