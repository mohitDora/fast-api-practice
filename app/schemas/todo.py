from pydantic import BaseModel, Field
from typing import Optional

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the todo item")
    description: Optional[str] = Field(None, max_length=500, description="A brief description of the todo item")
    completed: bool = Field(False, description="Indicates whether the todo item is completed")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="The title of the todo item")
    description: Optional[str] = Field(None, max_length=500, description="A brief description of the todo item")
    completed: Optional[bool] = Field(None, description="Indicates whether the todo item is completed")

class TodoOut(TodoBase):
    id: int = Field(..., description="The unique identifier of the todo item")
    user_id: int = Field(..., description="The unique identifier of the owner of the todo item")
    
    class Config:
        from_attributes = True