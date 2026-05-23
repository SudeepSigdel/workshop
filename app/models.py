from sqlmodel import SQLModel, Field, Column, TIMESTAMP, Integer, ForeignKey, Relationship
from datetime import datetime

class UserBase(SQLModel):
    email: str =Field(unique=True)
    password: str

class User(UserBase, table=True):
    __tablename__ = "users" #type:ignore

    id: int | None= Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.utcnow(), sa_column=Column(TIMESTAMP(timezone=True)))

class UserCreate(UserBase):
    pass

class UserResponse(SQLModel):
    id: int
    email: str
    created_at: datetime

class PostBase(SQLModel):
    title: str
    content: str
    published: bool | None =Field(default=True)


class Post(PostBase, table=True):
    __tablename__ = "posts" #type:ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None =Field(default=datetime.utcnow(), sa_column=Column(TIMESTAMP(timezone=True)))
    owner_id: int = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete=("CASCADE"))))
    owner: User= Relationship()

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse