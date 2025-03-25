

from ..models import Post
from ..schemas import PostInput, PostOutput, TokenData
from ..database import get_session
from fastapi import status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select
from ..utils import hash
from ..oauth2 import get_current_user



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.get("/", response_model=list[PostOutput])
def get_posts(db : Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    posts = db.exec(select(Post)).all()
    #NOTE - If I wanna show just lits the posts of the user that is logged in
    # posts = db.exec(select(Post).where(Post.owner_id == current_user.user_id)).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOutput)
def create_post(post: PostInput, db: Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    new_post = Post(owner_id=current_user.user_id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{post_id}", response_model=PostOutput)
def get_post(post_id: int, db: Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    post = db.get(Post, post_id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    
    #NOTE - If I wanna get just the post of the user that is logged in
    #if post.owner_id != current_user.user_id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to see this post")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    
    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this post")

    db.delete(post)
    db.commit()
    return

@router.put("/bug/{post_id}", response_model=PostOutput)
def update_post_with_dug(post_id: int, post: PostInput, db: Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    
    post_to_update = db.get(Post, post_id)
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this post")
    
    update_data = post.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_to_update, key, value)

    db.add(post_to_update)
    db.commit()
    db.refresh(post_to_update)
    return post_to_update

@router.put("/{post_id}", response_model=PostOutput)
def update_post(post_id: int, post: PostInput, db: Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    post_to_update = db.get(Post, post_id)
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    if post_to_update.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this post")
    
    update_data = post.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_to_update, key, value)

    db.commit()
    db.refresh(post_to_update)
    return post_to_update