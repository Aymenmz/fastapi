from ..models import User
from ..schemas import UserInput, UserOutput
from ..database import get_session
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlmodel import Session
from ..utils import hash


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)





@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOutput)
def create_user(user: UserInput, db: Session = Depends(get_session)):
    # hash the password
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserOutput)
def get_user(id: int, db: Session = Depends(get_session)):
    user = db.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    return user