from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.todo import TodoCreate, TodoUpdate, TodoOut
from app.services.todo import create_todo, get_todo, get_todos, update_todo, delete_todo
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/todos", response_model=TodoOut)
def create_todo_item(todo:TodoCreate,db:Session=Depends(get_db)):
    db_todo = create_todo(db, todo)
    return db_todo

@router.get("/todos/{todo_id}", response_model=TodoOut)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.get("/todos", response_model=List[TodoOut])
def read_todos(db: Session = Depends(get_db)):
    todos = get_todos(db)
    return todos

@router.put("/todos/{todo_id}", response_model=TodoOut)
def update_todo_item(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = update_todo(db, todo_id, todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/todos/{todo_id}", response_model=dict)
def delete_todo_item(todo_id: int, db: Session = Depends(get_db)):
    success = delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted successfully"}