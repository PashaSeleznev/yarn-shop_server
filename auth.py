"""
Хеширование и проверка паролей

Функционал:
- hash_password: принимает пароль, возвращает хеш (алгоритм Argon2)
- verify_password: сравнивает пароль с хешом, возвращает bool

Примечания:
- Используется библиотека passlib с алгоритмом Argon2 (современный стандарт)
- Argon2 устойчив к атакам перебор
"""

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)