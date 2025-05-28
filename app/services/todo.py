from sqlalchemy.orm import Session
from app.db.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

def create_todo(db: Session, todo: TodoCreate) -> Todo:
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo(db: Session, todo_id: int) -> Todo:
    return db.query(Todo).filter(Todo.id == todo_id).first()

def get_todos(db:Session):
    return db.query(Todo).all()

def update_todo(db: Session, todo_id: int, todo: TodoUpdate) -> Todo:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return None
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int) -> bool:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return False
    db.delete(db_todo)
    db.commit()
    return True