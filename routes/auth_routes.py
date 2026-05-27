from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.user_controller import UserController
from pydantic import BaseModel, Field

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegister(BaseModel):
    username: str = Field(..., min_length=4)
    name: str = Field(..., min_length=4)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    return UserController.register(db, user.dict())

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return UserController.login(db, user.dict())
