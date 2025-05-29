from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.auth.security import hash_password, verify_password

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, userLogin:UserLogin):
    user = get_user_by_username(db, userLogin.username)
    if not user or not verify_password(userLogin.password, user.hashed_password):
        return False
    return user