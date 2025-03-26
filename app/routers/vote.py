from ..models import Vote, Post
from ..schemas import VoteInput, TokenData
from ..database import get_session
from fastapi import status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select
from ..oauth2 import get_current_user
from typing import Optional


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote_input: VoteInput,
    db: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
):
    post = db.get(Post, vote_input.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote_input.post_id} does not exist"
        )
    existing_vote = db.exec(
        select(Vote).where(
            Vote.post_id == vote_input.post_id,
            Vote.user_id == current_user.user_id
        )
    ).first()

    # User is trying to upvote
    if vote_input.direction == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.user_id} already voted on post {vote_input.post_id}"
            )
        new_vote = Vote(user_id=current_user.user_id, post_id=vote_input.post_id, direction=1)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote registered"}

    # User is trying to remove vote
    else:
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existing vote to remove for user {current_user.user_id} on post {vote_input.post_id}"
            )
        db.delete(existing_vote)
        db.commit()
        return {"message": "Vote removed"}

