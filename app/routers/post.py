

from ..models import Post, Vote
from ..schemas import PostInput, PostOutput, TokenData, PostWithVotes
from ..database import get_session
from fastapi import status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select, func
from ..utils import hash
from ..oauth2 import get_current_user
from typing import Optional



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



"""
    The get_posts function is responsible for returning a list of posts.
    It receives the following parameters: db, current_user, limit, skip, and search.
    The db parameter is the database session, current_user is the user that is logged in, limit is the number of posts to return, skip is the number of posts to skip, and search is the search term to filter the posts.
    The function executes a query to get the posts from the database, filters the posts by the search term, and returns the list of posts.
    The function uses the get_session and get_current_user dependencies to get the database session and the current user.
    The function returns a list of PostOutput objects.
"""
@router.get("/", response_model=list[PostOutput])
def get_posts(db : Session = Depends(get_session), current_user: TokenData = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    statement = select(Post).where(Post.title.contains(search)).limit(limit).offset(skip)
    posts = db.exec(statement).all()

    #NOTE - If I wanna show just lits the posts of the user that is logged in
    # posts = db.exec(select(Post).where(Post.owner_id == current_user.user_id)).all()
    return posts

@router.get("/votes", response_model=list[PostWithVotes])
def get_posts_with_votes(
    db: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user),
    limit: int = 10, 
    skip: int = 0,
    search: Optional[str] = ""
):
    statement = (
        select(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .where(func.lower(Post.title).contains(search.lower()))
        .group_by(Post.id).limit(limit).offset(skip)
    )

    results = db.exec(statement).all()  

    response = [
        {
            "post": post,
            "votes": votes
        }
        for post, votes in results
    ]

    return response


"""
    The create_post function is responsible for creating a new post.
    It receives the following parameters: post, db, and current_user.
    The post parameter is the post data, db is the database session, and current_user is the user that is logged in.
    The function creates a new Post object with the data from the post parameter, adds the post to the database, commits the transaction, and returns the new post.
    The function uses the get_session and get_current_user dependencies to get the database session and the current user.
    The function returns a PostOutput object.

"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOutput)
def create_post(post: PostInput, db: Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    new_post = Post(owner_id=current_user.user_id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


"""
    The get_post function is responsible for returning a post by its id.
    It receives the following parameters: post_id, db, and current_user.
    The post_id parameter is the id of the post, db is the database session, and current_user is the user that is logged in.
    The function executes a query to get the post by its id, checks if the post exists, and returns the post.
    The function uses the get_session and get_current_user dependencies to get the database session and the current user.
    The function returns a PostOutput object.
"""
@router.get("/{post_id}", response_model=PostOutput)
def get_post(post_id: int, db: Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    post = db.get(Post, post_id)
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    
    #NOTE - If I wanna get just the post of the user that is logged in
    #if post.owner_id != current_user.user_id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to see this post")
    return post

@router.get("/votes/{post_id}", response_model=PostWithVotes)
def get_post(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
):
    statement = (
        select(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .where(Post.id == post_id) 
        .group_by(Post.id)
    )

    result = db.exec(statement).first() 
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    post, votes = result
    return {"post": post, "votes": votes}



"""
    The delete_post function is responsible for deleting a post by its id.
    It receives the following parameters: post_id, db, and current_user.
    The post_id parameter is the id of the post, db is the database session, and current_user is the user that is logged in.
    The function executes a query to get the post by its id, checks if the post exists, checks if the user is the owner of the post, deletes the post, commits the transaction, and returns a 204 No Content response.
    The function uses the get_session and get_current_user dependencies to get the database session and the current user.
    The function returns a 204 No Content response.

"""
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

"""
    The update_post function is responsible for updating a post by its id.
    It receives the following parameters: post_id, post, db, and current_user.
    The post_id parameter is the id of the post, post is the post data, db is the database session, and current_user is the user that is logged in.
    The function executes a query to get the post by its id, checks if the post exists, checks if the user is the owner of the post, updates the post with the data from the post parameter, commits the transaction, and returns the updated post.
    The function uses the get_session and get_current_user dependencies to get the database session and the current user.
    The function returns a PostOutput object.

"""
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


"""
    The update_post function is responsible for updating a post by its id.
    It receives the following parameters: post_id, post, db, and current_user.
    The post_id parameter is the id of the post, post is the post data, db is the database session, and current_user is the user that is logged in.
    The function executes a query to get the post by its id, checks if the post exists, checks if the user is the owner of the post, updates the post with the data from the post parameter, commits the transaction, and returns the updated post.
    The function uses the get_session and get_current_user dependencies to get the database session and the current user.
    The function returns a PostOutput object.

"""
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