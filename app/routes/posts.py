from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlmodel import select
from ..database import SESSION
from ..models import Post, PostCreate, PostResponse
from typing import List
from ..oauth2 import get_current_user

router = APIRouter(
    tags=["Post Endpoints"]
)

@router.get("/posts", response_model=List[PostResponse])
def get_all_post(db: SESSION):
    Posts = db.exec(select(Post)).all()
    return Posts

@router.get("/posts/{id}", response_model=PostResponse)
def get_one_post(id: int, db: SESSION):
    post = db.get(Post, id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")

@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(postdata: PostCreate, db: SESSION, user= Depends(get_current_user)):
    post = Post(owner_id=user.id, **postdata.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SESSION, user=Depends(get_current_user)):
    post = db.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")
    
    if not post.owner_id==user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can delete post")
    

    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model=PostResponse)
def update_post(id: int, postdata: PostCreate, db: SESSION, user=Depends(get_current_user)):
    post= db.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")

    if not post.owner_id==user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can Update post")

    new_post= postdata.model_dump()
    for key, value in new_post.items():
        setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post