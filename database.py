"""
Настройка подключения к базе данных

Функционал:
- Создание движка SQLAlchemy для PostgreSQL
- Создание фабрики сессий (SessionLocal)
- get_db: генератор сессий для Dependency Injection в FastAPI

Примечания:
- Порт PostgreSQL по умолчанию: 5432
- Сессия автоматически закрывается после завершения запроса
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_USER, DB_NAME, DB_PASSWORD


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
