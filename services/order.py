from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None
) -> Order:
    with transaction.atomic():
        user, _ = User.objects.get_or_create(
            username=username
        )
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()

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
        user = User.objects.get(username=username)
        orders = user.orders.all()
    else:
        orders = Order.objects.all()
    return orders
