from sqlmodel import SQLModel, Field, Column, TIMESTAMP
from datetime import datetime

class PostBase(SQLModel):
    title: str
    content: str
    published: bool | None =Field(default=True)


class Post(PostBase, table=True):
    __tablename__ = "post" #type:ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None =Field(default=datetime.utcnow(), sa_column=Column(TIMESTAMP(timezone=True)))

class PostCreate(PostBase):
    pass
