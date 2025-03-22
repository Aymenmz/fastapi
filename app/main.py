from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]
app = FastAPI(middleware=middleware)

class Post(BaseModel):
    title: str
    content: str
    published: bool = False

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor 
        )
        cur = conn.cursor()
        print("Connected to the database") 
        break
    except Exception as e:
        print(e)
        time.sleep(2)

my_posts = [
    {"id": 1, "title": "Post 3", "content": "This is the content of post 3"},
    {"id": 2, "title": "Post 4", "content": "This is the content of post 4"}  
]

def find_post_by_id(post_id):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    return None


@app.get("/")
def root():
    cur.execute("SELECT * FROM posts")
    my_posts = cur.fetchall()
    return {"data": my_posts}

@app.get("/posts")
def get_posts():
    return [

        {"title": "Post 1", "content": "This is the content of post 1"},
        {"title": "Post 2", "content": "This is the content of post 2"},
    ]

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cur.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    conn.commit()
    new_post = cur.fetchone()
    return {"data": new_post}                                                                                                                                                                                                                     


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int):
    cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} was not found")
    return {"data": post}

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(post_id: int):
    cur.execute("DELETE FROM posts WHERE id = %s returning *", (post_id,))
    deleted_post = cur.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post_by_id(post_id: int, updated_post: Post):
    cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *", (updated_post.title, updated_post.content, updated_post.published, post_id))
    updated_post = cur.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} was not found")
    
    return {"data": updated_post}

