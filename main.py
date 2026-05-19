"""
Главный файл приложения FastAPI

Эндпоинты:
- USERS: POST /users/ (регистрация), POST /login (авторизация), GET /users/{user_id} (получение данных о пользователе),
  DELETE /users/{user_id} (удаление пользователя)
- ORDERS: POST /orders/ (создание заказа и платежа), GET /orders/{order_id} (проверка статуса)

Функционал:
- Регистрация с хешированием пароля
- Авторизация (проверка email и пароля)
- Создание заказа → генерация UUID → создание платежа в ЮKassa → фоновый мониторинг оплаты
- При оплате статус меняется на 'paid', при отмене — на 'cancelled'

Примечания:
- CORS разрешён для http://localhost:5173
- База данных создаётся автоматически (models.Base.metadata.create_all)
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db
from auth import hash_password, verify_password
from payment_service import create_yookassa_payment, monitor_payment
import uuid


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)


# ============= USERS =============

@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login", response_model=schemas.UserOut)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return db_user


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


# ============= ORDERS =============

@app.post("/orders/")
def create_order(
    order_data: schemas.OrderCreate,
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    order_id = str(uuid.uuid4())

    db_order = models.Order(
        paymentId=order_id,
        amount=order_data.amount,
        status='pending',
        user_id=user_id,
        address=order_data.address
    )
    db.add(db_order)
    db.flush()

    for item in order_data.items:
        db_item = models.OrderItem(
            name=item.name,
            color=item.color,
            price=item.price,
            quantity=item.quantity,
            image=item.image,
            order_id=db_order.paymentId
        )
        db.add(db_item)

    db.commit()

    return_url = f"http://localhost:5173/?order_id={order_id}"
    payment_url, yookassa_payment_id = create_yookassa_payment(
        amount=order_data.amount,
        order_id=order_id,
        user_id=user_id,
        return_url=return_url
    )

    background_tasks.add_task(monitor_payment, yookassa_payment_id, db, order_id)

    return {"payment_url": payment_url, "order_id": order_id}


@app.get("/orders/{order_id}")
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.paymentId == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"status": order.status}
