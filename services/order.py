from db.models import Ticket, Order, User
from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order,
            )


def get_orders(username: str = None) -> QuerySet:
    order = Order.objects.all()
    if username:
        return order.filter(user__username=username)
    return order
