from datetime import datetime
from beanie import Document, PydanticObjectId
from pydantic import Field
from bson.objectid import ObjectId


class UsersDocument(Document):
    nm_name: str = ""
    nm_email: str = ""
    nm_password: str = ""
    is_active: bool = False
    is_superuser: bool = False
    date_created: datetime = datetime.now()

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "nm_name": "A",
            "nm_email": "A sample content",
            "nm_password": "A sample content",
            "is_active": True,
            "is_superuser": True,
            "date_created": datetime.now(),
        }

class UserCreateDocument(Document):
    nm_name: str = ""
    nm_email: str = ""
    nm_password: str = ""
    is_active: bool = False
    is_superuser: bool = False
    date_created: datetime = datetime.now()

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "nm_name": "A",
            "nm_email": "A sample content",
            "nm_password": "A sample content",
            "is_active": True,
            "is_superuser": True,
            "date_created": datetime.now(),
        }