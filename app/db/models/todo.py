from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.session import Base
from sqlalchemy.orm import relationship

class Todo(Base):
    __tablename__ = "todos"

    id=Column(Integer, primary_key=True, index=True)
    title=Column(String(100), nullable=False)
    description=Column(String(500), nullable=True)
    completed=Column(Boolean, default=False)
    user_id=Column(Integer, ForeignKey("usersV2.id"))

    owner = relationship("User", back_populates="todos")