from pydantic import BaseModel
from datetime import datetime

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str

# class DocumentOut(BaseModel):
#     id: int
#     filename: str
#     content: str
#     uploaded_at: datetime
class DocumentResponse(BaseModel):
    id: int
    filename: str
    content: str

    class Config:
        orm_mode = True