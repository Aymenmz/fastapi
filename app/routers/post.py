

from ..models import Post
from ..schemas import PostInput, PostOutput
from ..database import get_session
from fastapi import status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select
from ..utils import hash



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.get("/", response_model=list[PostOutput])
def get_posts(db : Session = Depends(get_session)):
    posts = db.exec(select(Post)).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOutput)
def create_post(post: PostInput, db: Session = Depends(get_session)):
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{post_id}", response_model=PostOutput)
def get_post(post_id: int, db: Session = Depends(get_session)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_session)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")

    db.delete(post)
    db.commit()
    return

@router.put("/bug/{post_id}", response_model=PostOutput)
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

@router.put("/{post_id}", response_model=PostOutput)
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