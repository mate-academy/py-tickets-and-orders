from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
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


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        orders = orders.filter(user=user)
    return orders
