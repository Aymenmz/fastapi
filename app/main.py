from fastapi import FastAPI, status, HTTPException, Depends
from .database import lifespan, get_session
from sqlmodel import Session, select
from  .models import Post, User
from .schemas import PostInput, PostOutput, UserInput, UserOutput


app = FastAPI(lifespan=lifespan)




@app.get("/")
def root():
    return {"data": "Hello World from FastAPI"}

@app.get("/posts", response_model=list[PostOutput])
def get_posts(db : Session = Depends(get_session)):
    posts = db.exec(select(Post)).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostOutput)
def create_post(post: PostInput, db: Session = Depends(get_session)):
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{post_id}", response_model=PostOutput)
def get_post(post_id: int, db: Session = Depends(get_session)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_session)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")

    db.delete(post)
    db.commit()
    return

@app.put("/posts/bug/{post_id}", response_model=PostOutput)
def update_post_with_dug(post_id: int, post: PostInput, db: Session = Depends(get_session)):
    post_to_update = db.get(Post, post_id)
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    
    update_data = post.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_to_update, key, value)

    db.add(post_to_update)
    db.commit()
    db.refresh(post_to_update)
    return post_to_update

@app.put("/posts/{post_id}", response_model=PostOutput)
def update_post(post_id: int, post: PostInput, db: Session = Depends(get_session)):
    post_to_update = db.get(Post, post_id)
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    
    update_data = post.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_to_update, key, value)

    db.commit()
    db.refresh(post_to_update)
    return post_to_update

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOutput)
def create_user(user: UserInput, db: Session = Depends(get_session)):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

