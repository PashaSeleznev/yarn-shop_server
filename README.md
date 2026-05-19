# Магазин пряжи (Backend)

## Описание

Backend-часть интернет-магазин для продажи пряжи и аксессуаров для вязания.

Основные технологии:
- FastAPI (Python)
- PostgreSQL (база данных)
- SQLAlchemy (ORM)
- ЮKassa (платёжная система)
- FastAPI-Mail (email уведомления)

---

## Структура проекта

```
server/
├── auth.py
├── config.py
├── database.py
├── email_service.py
├── main.py
├── models.py
├── payment_service.py
├── schemas.py
|
├── venv
├── .env
├── requirements.txt

```
---

## Функционал API

### Пользователи
- `POST /users/` — регистрация
- `POST /login` — авторизация
- `GET /users/{user_id}` — получение данных пользователя
- `DELETE /users/{user_id}` — удаление пользователя

### Заказы
- `POST /orders/` — создание заказа и платежа в ЮKasse
- `GET /orders/{order_id}` — проверка статуса заказа

---

## Запуск проекта

### 1. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Создайте файл .env по образцу:
```bash
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=shop_db

YOOKASSA_SHOP_ID=your_shop_id
YOOKASSA_SECRET_KEY=your_secret_key

MAIL_USERNAME=your_email@mail.ru
MAIL_PASSWORD=your_password
MAIL_FROM=your_email@mail.ru
MAIL_SERVER=smtp.mail.ru
MAIL_PORT=465
MAIL_SELLER=seller@example.com
```

### 4. Запуск сервера
```bash
uvicorn main:app --reload
```

---

Frontend-часть находится в другом репозитории: https://github.com/PashaSeleznev/yarn-shop_client
