from fastapi import FastAPI
from .database import create_table
from .routes import posts, users, login

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_table()

app.include_router(users.router)
app.include_router(login.router)
app.include_router(posts.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}