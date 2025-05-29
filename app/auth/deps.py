from fastapi import Depends, HTTPException
from app.auth.auth import verify_token
from app.db.session import SessionLocal
from app.services.user import get_user_by_username
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_cuurent_user(token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    db=SessionLocal()
    user = get_user_by_username(db, payload["sub"])
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user