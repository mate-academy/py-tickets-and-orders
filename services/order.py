from datetime import datetime

import django.db.transaction

from db.models import Order
from db.models import User
from db.models import Ticket


def create_order(tickets: dict, username: str, date: datetime = None) -> None:
    with django.db.transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> list[Order]:
    order_query_set = Order.objects.all()
    if username:
        order_query_set = order_query_set.filter(user__username=username)
    return order_query_set
