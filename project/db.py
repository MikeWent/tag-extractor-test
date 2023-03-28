from os import getenv
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
