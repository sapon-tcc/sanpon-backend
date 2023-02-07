from fastapi import APIRouter, HTTPException, Depends
from app.documents.users.user import UsersDocument, UserCreateDocument
from app.core import security
from app.auth.auth import get_current_active_user
from typing import List
from beanie import PydanticObjectId
from bson import ObjectId

user_router = APIRouter()

@user_router.get("/", status_code=200)
async def retrieve_users(current_user: UserCreateDocument = Depends(get_current_active_user)) -> List[UsersDocument]:
    users = await UsersDocument.find_all(limit=1000).to_list()
    return users

@user_router.get("/{user_id}", status_code=200)
async def retrieve_user(user_id: PydanticObjectId) -> UsersDocument:
    user = await UsersDocument.get(user_id)
    return user

@user_router.post("/", status_code=201)
async def create_user(user: UserCreateDocument):
    user.nm_password = security.get_password_hash(user.nm_password)
    if await user.find_one({"nm_email": user.nm_email}):
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    await user.create()
    return {"message": "User has been saved"}

@user_router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: PydanticObjectId):
    user = await UsersDocument.get(user_id)
    await user.delete()
    return {"message": "User deleted"}

@user_router.put("/{user_id}", status_code=200)
async def update_user(user: UserCreateDocument, user_id: PydanticObjectId) -> UsersDocument:

    user_to_update = await UsersDocument.get(user_id)
    if not user_to_update:
        raise HTTPException(status_code=404, detail="Resource not found")

    user_to_update.nm_email = user.nm_email
    user_to_update.nm_name = user.nm_name
    await user_to_update.save()
    return user_to_update

