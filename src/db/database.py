from sqlalchemy import create_engine
from sqlalchemt.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # base class for our models

from core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Called by the dependency injection system to get a database session for each request.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Called when the application starts to create the tables in the database.
def create_tables():
    Base.metadata.create_all(bind=engine)