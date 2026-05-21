from fastapi import APIRouter, HTTPException, status, Response
from sqlmodel import select
from ..database import SESSION
from ..models import Post, PostCreate
from typing import List

router = APIRouter(
    tags=["Post Endpoints"]
)

@router.get("/posts", response_model=List[Post])
def get_all_post(db: SESSION):
    Posts = db.exec(select(Post)).all()
    return Posts

@router.get("/posts/{id}")
def get_one_post(id: int, db: SESSION):
    post = db.get(Post, id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")

@router.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(postdata: PostCreate, db: SESSION):
    post = Post(**postdata.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SESSION):
    post = db.get(Post, id)
    if post:
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")


@router.put("/posts/{id}", response_model=Post)
def update_post(id: int, postdata: PostCreate, db: SESSION):
    post= db.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")

    new_post= postdata.model_dump()
    for key, value in new_post.items():
        setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post