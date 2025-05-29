from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="The username of the user")
    email: EmailStr = Field(..., description="The email of the user")
    password: str = Field(..., min_length=8, description="The password of the user")

class UserOut(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=20, description="The username of the user")
    email: EmailStr = Field(..., description="The email of the user")

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="The username of the user")
    password: str = Field(..., min_length=8, description="The password of the user")

class Token(BaseModel):
    access_token: str
    token_type: str