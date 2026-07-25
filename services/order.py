from django.db.models import QuerySet
from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order:
    user_model = get_user_model()
    # Шукаємо користувача безпосередньо за username
    user = user_model.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        # Парсимо рядок у справжній об'єкт datetime
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
