from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.todo import TodoCreate, TodoUpdate, TodoOut
from app.services.todo import create_todo, get_todo, get_todos, update_todo, delete_todo, get_user_todos
from app.auth.deps import get_cuurent_user
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/todos", response_model=TodoOut)
def create_todo_item(todo:TodoCreate,db:Session=Depends(get_db), current_user = Depends(get_cuurent_user)):
    db_todo = create_todo(db, todo, current_user)
    return db_todo

@router.get("/todos/user", response_model=List[TodoOut])
def read_user_todos( db: Session = Depends(get_db),current_user = Depends(get_cuurent_user)):
    todos = get_user_todos(db, current_user)
    return todos

@router.get("/todos/{todo_id}", response_model=TodoOut)
def read_todo(todo_id: int, db: Session = Depends(get_db),current_user = Depends(get_cuurent_user)):
    db_todo = get_todo(db, todo_id, current_user)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.get("/todos", response_model=List[TodoOut])
def read_todos(db: Session = Depends(get_db),current_user = Depends(get_cuurent_user)):
    todos = get_todos(db)
    return todos

@router.put("/todos/{todo_id}", response_model=TodoOut)
def update_todo_item(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db),current_user = Depends(get_cuurent_user)):
    db_todo = update_todo(db, todo_id, todo, current_user)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/todos/{todo_id}", response_model=dict)
def delete_todo_item(todo_id: int, db: Session = Depends(get_db),current_user = Depends(get_cuurent_user)):
    success = delete_todo(db, todo_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted successfully"}