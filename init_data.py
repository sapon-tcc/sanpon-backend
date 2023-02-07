import logging

#from app.database.init_data import init_data
from app.database.session import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# TODO: To criando...

# def init() -> None:
#     db = SessionLocal()
#     init_db(db)


# def main() -> None:
#     logger.info("Creating initial data")
#     init()
#     logger.info("Initial data created")


# if __name__ == "__main__":
#     main()
