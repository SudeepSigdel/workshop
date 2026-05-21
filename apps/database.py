from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated
from fastapi import Depends
from .config import settings

DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SESSION = Annotated[Session, Depends(get_session)]

def create_table():
    SQLModel.metadata.create_all(engine)