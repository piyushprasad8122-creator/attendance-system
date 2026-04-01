from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    department: str
    role: Optional[str] = "employee"  # employee or admin

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    department: str
    role: str
    created_at: datetime
