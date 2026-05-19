"""
Работа с платёжной системой ЮKassa

Функционал:
- create_yookassa_payment: создаёт платёж, возвращает ссылку для оплаты и ID платежа
- monitor_payment: асинхронный мониторинг статуса платежа (каждые 5 секунд)

Примечания:
- При успешной оплате обновляет статус заказа на 'paid' и отправляет письма пользователю
- При отмене обновляет статус на 'cancelled'
"""

from yookassa import Configuration, Payment
import asyncio
from sqlalchemy.orm import Session
import models
from config import YOOKASSA_SECRET_KEY, YOOKASSA_SHOP_ID
from email_service import send_order_emails


Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


def create_yookassa_payment(amount: float, order_id: str, user_id: int, return_url: str):
    """
    Создает платеж в ЮKassa
    Возвращает (payment_url, yookassa_payment_id)
    """
    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "description": f"Заказ #{order_id[:8]}",
        "metadata": {
            "order_id": order_id,
            "user_id": str(user_id)
        }
    })

    payment_url = payment.confirmation.confirmation_url
    yookassa_payment_id = payment.id

    return payment_url, yookassa_payment_id


async def monitor_payment(yookassa_payment_id: str, db: Session, order_id: str):
    print(f"🔄 Начинаю мониторинг платежа {yookassa_payment_id} для заказа {order_id}")

    while True:
        try:
            payment = Payment.find_one(yookassa_payment_id)

            if payment.status == "succeeded":
                print(f"🎉 Платеж {yookassa_payment_id} успешен! Обновляю статус заказа...")

                order = db.query(models.Order).filter(models.Order.paymentId == order_id).first()
                if order:
                    order.status = 'paid'
                    db.commit()
                    print(f"✅ Заказ {order_id} обновлен на 'paid'")

                    # 👇 Отправка писем (теперь ДО break)
                    user = db.query(models.User).filter(models.User.id == order.user_id).first()
                    items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()

                    await send_order_emails(
                        order_id=order_id,
                        user_email=user.email,
                        order_amount=order.amount,
                        order_address=order.address,
                        items=items
                    )

                break

            elif payment.status == "canceled":
                print(f"❌ Платеж {yookassa_payment_id} отменен")
                order = db.query(models.Order).filter(models.Order.paymentId == order_id).first()
                if order:
                    order.status = 'cancelled'
                    db.commit()
                break

            else:
                print(f"⏳ Платеж {yookassa_payment_id}: статус {payment.status}, жду...")
                await asyncio.sleep(5)

        except Exception as e:
            print(f"⚠️ Ошибка при проверке платежа {yookassa_payment_id}: {e}")
            await asyncio.sleep(10)