import datetime

from django.contrib.auth import get_user_model

from django.db import transaction

from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.date = None,
) -> Order:

    user = get_user_model().objects.get(username=username)

    # Збираємо дані для створення
    order_data = {"user": user}
    if date:
        order_data["created_at"] = date

    # Створюємо ордер ОДИН раз із потрібною датою
    order = Order.objects.create(**order_data)

    # Зайвий блок з update() ми повністю видалили!

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
