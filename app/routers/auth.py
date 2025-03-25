from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ..models import User
from ..schemas import Token
from ..database import get_session
from ..utils import hash, verify
from ..oauth2 import create_access_token


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.username)
    user_exist = db.exec(statement).first()

    if not user_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not verify(user.password, user_exist.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    token = create_access_token(data={"user_id": user_exist.id})
    return {"access_token": token, "token_type": "bearer"}
