"""
Модели базы данных для SQLAlchemy

Структура:
- User: пользователи (id, username, email, password)
- Order: заказы (paymentId, amount, date, status, user_id, address)
- OrderItem: товары в заказе (id, name, color, image, price, quantity, order_id)

Связи:
- User → Order: один ко многим (один пользователь — много заказов)
- Order → OrderItem: один ко многим (один заказ — много товаров)

Примечания:
- paymentId — первичный ключ (UUID от ЮKassa)
- При удалении пользователя удаляются его заказы (ondelete="CASCADE")
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "orders"

    paymentId = Column(String(255), primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    address = Column(String(500), nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    color = Column(String(100), nullable=False)
    image = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_id = Column(String(255), ForeignKey("orders.paymentId", ondelete="CASCADE"))

    order = relationship("Order", back_populates="items")