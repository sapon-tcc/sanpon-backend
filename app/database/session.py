import beanie
import motor
import motor.motor_asyncio
from app.documents.users.user import UsersDocument, UserCreateDocument
from app.core.config import settings

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
    await beanie.init_beanie(database=client.sapon, document_models=[UsersDocument, UserCreateDocument])