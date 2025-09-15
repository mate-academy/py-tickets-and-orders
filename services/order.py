from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None
) -> Order:
    user, _ = get_user_model().objects.get_or_create(
        username=username
    )
    order = Order.objects.create(created_at=date, user=user)

    for ticket in tickets:
        row = int(ticket["row"])
        seat = int(ticket["seat"])
        movie_session_id = ticket["movie_session"]

        Ticket.objects.create(
            order=order,
            row=row,
            seat=seat,
            movie_session_id=movie_session_id
        )

    return order


def get_orders(
        username: str=None
) -> QuerySet[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        orders = user.orders.all()
    else:
        orders = Order.objects.all()
    return orders
