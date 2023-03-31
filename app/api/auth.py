from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services import auth, user as user_service
from app.models.user import User
from app.schemas.user import Token, UserLogin, TokenRefresh
from app.database import SessionLocal
from app.services.auth import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db, username=user_login.username)
    if not db_user or not user_service.verify_password(user_login.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_refresh_token(data={"sub": db_user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh-token", response_model=Token)
async def refresh_token(token_refresh: TokenRefresh, db: Session = Depends(get_db)):
    try:
        payload = decode_refresh_token(token_refresh.refresh_token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        access_token = create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/logout")
async def logout(refresh_token: TokenRefresh, db: Session = Depends(get_db)):
    try:
        payload = decode_refresh_token(refresh_token.refresh_token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"detail": "Logged out"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
