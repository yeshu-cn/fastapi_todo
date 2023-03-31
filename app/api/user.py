from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import user as user_service
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.create_user(db=db, user=user)
