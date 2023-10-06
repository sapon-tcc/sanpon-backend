from datetime import datetime
from beanie import Document


class BookDocument(Document):
    nm_title: str = ""
    date_created: datetime = datetime.now()

    class Settings:
        name = "books"

    class Config:
        schema_extra = {
            "nm_title": "Harry Potter",
        }
