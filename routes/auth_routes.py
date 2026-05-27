from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.user_controller import UserController
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegister(BaseModel):
    username: str
    name: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    return UserController.register(db, user.dict())

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return UserController.login(db, user.dict())
