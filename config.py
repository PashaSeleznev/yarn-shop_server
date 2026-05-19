"""
Конфигурация приложения из переменных окружения

Переменные:
- База данных: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
- ЮKassa: YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY
- Почта: MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_SERVER, MAIL_PORT

Примечания:
- Значения берутся из .env файла (через python-dotenv)
- MAIL_SERVER и MAIL_PORT имеют значения по умолчанию (smtp.mail.ru, 465)
"""

import os
from dotenv import load_dotenv


load_dotenv()


# База данных
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# ЮKassa
YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")


# Почта
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.mail.ru")
MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
MAIL_SELLER = os.getenv("MAIL_SELLER")