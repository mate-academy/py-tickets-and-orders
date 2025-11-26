from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime as dt
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str | None = None
) -> Order:

    order = Order(user=get_user_model().objects.get(username=username))

    if date:
        order.created_at = dt.strptime(date, "%Y-%m-%d %H:%M")

    order.save()

    for ticket in tickets:
        if Ticket.objects.filter(
            movie_session=ticket["movie_session"],
            seat=ticket["seat"],
            row=ticket["row"],
        ).exists():
            raise ValueError("Seat is already taken.")
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order,
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(
            user=get_user_model().objects.get(username=username)
        )
    return orders
