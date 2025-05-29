from sqlalchemy.orm import Session
from app.db.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

def create_todo(db: Session, todo: TodoCreate, current_user) -> Todo:
    db_todo = Todo(**todo.dict(), user_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo(db: Session, todo_id: int, current_user) -> Todo:
    todo=db.query(Todo).filter(Todo.id == todo_id).first()
    if todo.user_id != current_user.id:
        return None
    return todo

def get_todos(db:Session):
    return db.query(Todo).all()

def update_todo(db: Session, todo_id: int, todo: TodoUpdate, current_user) -> Todo:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo.user_id != current_user.id:
        return None
    if not db_todo:
        return None
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int, current_user) -> bool:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo.user_id != current_user.id:
        return False
    if not db_todo:
        return False
    db.delete(db_todo)
    db.commit()
    return True

def get_user_todos(db: Session, current_user) -> list[Todo]:
    print(type(current_user))
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()