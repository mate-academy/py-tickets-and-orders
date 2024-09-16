from datetime import datetime
from typing import List

from django.db import transaction

from db.models import Order, Ticket, User


def create_order(tickets: List[dict],
                 username: str = None,
                 date: datetime = None) -> Order:

    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(row=ticket["row"],
                                  seat=ticket["seat"],
                                  movie_session_id=ticket["movie_session"],
                                  order=order)
        return order


def get_orders(username: str = None) -> User:
    user = Order.objects.all().prefetch_related("user")
    if username:
        user = user.filter(user__username=username)
    return user
