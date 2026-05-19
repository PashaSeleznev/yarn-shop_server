"""
Pydantic схемы

Структура:
- USER SCHEMAS: регистрация, логин, ответ с данными пользователя
- ORDER SCHEMAS: создание заказа, ответ с заказом, ответ с платёжной ссылкой

Примечания:
- UserRegister: валидация username, email (не пустые) и password (мин. 6 символов)
- OrderCreate: address не менее 5 символов, items не может быть пустым
- OrderWithPaymentUrl наследуется от OrderOut и добавляет payment_url
"""

from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import List


# ============= USER SCHEMAS =============

class UserRegister(BaseModel):
    username: str = Field(..., min_length=2, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email должен быть корректным")
    password: str = Field(..., min_length=6, max_length=64, description="Пароль от 6 до 64 символов")

    @validator('username')
    def username_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Имя пользователя не может быть пустым')
        return v.strip()

    @validator('email')
    def email_not_empty(cls, v):
        if not v or not str(v).strip():
            raise ValueError('Email не может быть пустым')
        return v

    @validator('password')
    def password_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Пароль не может быть пустым')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ============= ORDER SCHEMAS =============

class OrderItemCreate(BaseModel):
    name: str
    color: str
    image: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    amount: float
    address: str = Field(..., min_length=5, max_length=500)
    items: List[OrderItemCreate] = Field(..., min_items=1)


class OrderItemOut(BaseModel):
    id: int
    name: str
    color: str
    image: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    paymentId: str
    amount: float
    date: datetime
    status: str
    address: str
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True


class OrderWithPaymentUrl(OrderOut):
    payment_url: str
    items: List[OrderItemCreate] = []

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    orders: List[OrderOut] = []

    class Config:
        from_attributes = True