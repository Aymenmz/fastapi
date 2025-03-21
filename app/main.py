from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware



from random import randrange



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
    return {"data": my_posts}

@app.get("/posts")
def get_posts():
    return [

        {"title": "Post 1", "content": "This is the content of post 1"},
        {"title": "Post 2", "content": "This is the content of post 2"},
    ]

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 10000000)
    my_posts.append(post_dict)
    print(my_posts)
    return {"data": post_dict}                                                                                                                                                                                                                     


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int, response: Response):
    post = find_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} was not found")
    return {"data": post}

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(post_id: int):
    post = find_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} was not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post_by_id(post_id: int, updated_post: Post):
    post = find_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} was not found")
    
    post["id"] = post_id
    post["title"] = updated_post.title
    post["content"] = updated_post.content
    post["published"] = updated_post.published
    post["rating"] = updated_post.rating
    return {"data": post}

