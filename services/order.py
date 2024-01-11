import datetime

from django.db import transaction

from db.models import Order, Ticket, User, MovieSession
from typing import List


def create_order(
        tickets: List[dict],
        username: str,
        date: datetime = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for tickets_data in tickets:
            Ticket.objects.create(
                row=tickets_data["row"],
                seat=tickets_data["seat"],
                movie_session=MovieSession.objects.get(
                    id=tickets_data["movie_session"]
                ),
                order=order
            )


def get_orders(username: str = None) -> Order:

    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders
