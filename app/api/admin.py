from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import user as user_service
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB
from app.database import SessionLocal
from typing import List
from app.services.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", response_model=List[UserInDB])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.isAdmin:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.isAdmin:
        raise HTTPException(status_code=403, detail="Forbidden")
    

    db_user = user_service.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserInDB)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.isAdmin:
        raise HTTPException(status_code=403, detail="Forbidden")
    

    db_user = user_service.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=int)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.isAdmin:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    deleted_user_id = user_service.delete_user(db, user_id)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user_id
