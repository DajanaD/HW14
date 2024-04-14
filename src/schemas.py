from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# Модель для контакту
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_data: Optional[str] = None

# Використовуємо введення користувача для створення нового контакту
class ContactCreate(ContactBase):
    pass

# Модель для виведення інформації про контакт користувачу
class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True

# Модель для користувача
class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr
