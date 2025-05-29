from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserLogin, UserOut, UserCreate, Token
from app.services.user import authenticate_user, get_user_by_username, create_user
from app.auth.auth import create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register(user:UserCreate, db:Session=Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = create_user(db, user)
    return db_user

@router.post("/login", response_model=Token)
def login(user:UserLogin, db:Session=Depends(get_db)):
    db_user = authenticate_user(db, user)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data = {"sub": db_user.username}) 
    return {"access_token": access_token, "token_type": "bearer"}