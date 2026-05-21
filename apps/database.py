from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "postgresql://postgres:password@localhost:5432/workshop"
# postgresql://{username}:{password}@{hostname}:{port}/{databaseName}

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SESSION = Annotated[Session, Depends(get_session)]

def create_table():
    SQLModel.metadata.create_all(engine)