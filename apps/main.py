from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

Posts = []

id = 1

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int

@app.get("/posts", response_model=List[Post])
def get_all_post():
    return Posts

@app.get("/posts/{id}")
def get_one_post(id: int):
    for post in Posts:
        if post.id == id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")

@app.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(postdata: PostCreate):
    
    global id
    post = Post(id=id, **postdata.dict())
    id += 1
    Posts.append(post)
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for post in Posts:
        if post.id == id:
            Posts.remove(post)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")


@app.put("/posts/{id}", response_model=Post)
def update_post(id: int, postdata: PostCreate):
    for post in Posts:
        if post.id == id:
            new_post = Post(id=id, **postdata.dict())
            Posts.remove(post)
            Posts.append(new_post)
            return post
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")