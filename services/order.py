import datetime
from typing import List

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: List[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date is not None:
            order.created_at = date
            order.save()
        for new_ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=new_ticket["row"],
                seat=new_ticket["seat"],
                movie_session_id=new_ticket["movie_session"]
            )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username is not None:
        orders = orders.filter(user__username=username)
    return orders
