from sqlalchemy.orm import Session
from models.user_model import User
from services.auth_service import AuthService
from fastapi import HTTPException, status

class UserController:
    @staticmethod
    def register(db: Session, user_data: dict):
        existing_user = db.query(User).filter(User.username == user_data['username']).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = AuthService.hash_password(user_data['password'])
        new_user = User(
            username=user_data['username'],
            name=user_data['name'],
            password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully"}

    @staticmethod
    def login(db: Session, user_data: dict):
        user = db.query(User).filter(User.username == user_data['username']).first()
        if not user or not AuthService.verify_password(user_data['password'], user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        token = AuthService.create_access_token(data={"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
