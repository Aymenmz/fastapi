from fastapi import FastAPI
from .database import lifespan
from .utils import hash
from .routers import post, user, auth

app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"data": "Hello World from FastAPI"}






