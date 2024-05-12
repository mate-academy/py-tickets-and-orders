from typing import List, Dict, Optional
from django.db import transaction
from db.models import Order, Ticket, User, MovieSession
from datetime import datetime


@transaction.atomic
def create_order(
        tickets: List[Dict[str, int]],
        username: str,
        date: Optional[str] = None
) -> Order:
    try:
        # Получаем пользователя по имени пользователя
        user = User.objects.get(username=username)

        # Создаем заказ и связываем его с пользователем
        order = Order.objects.create(user=user)

        # Обработка даты создания заказа, если она передана
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        # Создаем билеты для заказа
        for ticket_data in tickets:
            row = ticket_data.get("row")
            seat = ticket_data.get("seat")
            movie_session_id = ticket_data.get("movie_session")

            # Проверяем, существует ли сеанс с таким идентификатором
            movie_session = MovieSession.objects.get(id=movie_session_id)

            # Создаем билет и связываем его с заказом и сеансом
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=row, seat=seat
            )

        return order
    except Exception as e:
        # Если произошла ошибка, откатываем транзакцию
        transaction.set_rollback(True)
        raise e


def get_orders(username: Optional[str] = None) -> List[Order]:
    if username:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()
    return orders
