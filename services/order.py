from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)

    if date:
        order = Order.objects.create(
            created_at=date,
            user=user,
        )
    else:
        order = Order.objects.create(
            user=user
        )

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        user = User.objects.get(username=username)
        orders = Order.objects.filter(user=user)
        return orders
    else:
        return Order.objects.all()
