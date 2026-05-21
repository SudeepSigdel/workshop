from fastapi import FastAPI
from .database import create_table
from .routes import posts

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_table()

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

app.include_router(posts.router)