"""
Отправка email-уведомлений о заказах

Функционал:
- send_order_emails: отправляет два письма при успешной оплате заказа
  - Покупателю: подтверждение заказа с составом, суммой и адресом доставки
  - Продавцу: уведомление о новом заказе
"""

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_SERVER, MAIL_PORT, MAIL_SELLER

mail_conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_order_emails(order_id: str, user_email: str, order_amount: float, order_address: str, items: list):
    # Письмо покупателю
    items_text = "\n".join([
        f"- {item.name} ({item.color}): {item.quantity} шт. × {item.price} ₽ = {item.quantity * item.price} ₽"
        for item in items
    ])

    customer_body = f"""
    Заказ #{order_id[:8]} оформлен!

    Сумма: {order_amount} ₽
    Адрес доставки: {order_address}

    Состав заказа:
    {items_text}

    Спасибо за покупку!
    """

    customer_message = MessageSchema(
        subject=f"Заказ #{order_id[:8]} подтвержден",
        recipients=[user_email],
        body=customer_body,
        subtype=MessageType.plain
    )

    # Письмо продавцу
    seller_body = f"""
    НОВЫЙ ЗАКАЗ #{order_id}

    Покупатель: {user_email}
    Сумма: {order_amount} ₽
    Адрес: {order_address}

    Товары:
    {items_text}
    """

    seller_message = MessageSchema(
        subject=f"Новый заказ #{order_id[:8]}",
        recipients=[MAIL_SELLER],
        body=seller_body,
        subtype=MessageType.plain
    )

    fm = FastMail(mail_conf)
    await fm.send_message(customer_message)
    await fm.send_message(seller_message)
    print(f"📧 Письма отправлены для заказа {order_id}")