from django.db.models import QuerySet
from db.models import Ticket, Order
from django.db import transaction
from django.contrib.auth import get_user_model
from typing import List


def create_order(
        tickets: List[dict],
        username: str,
        date: int = None,
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
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
    orders = Order.objects.all().order_by("-id")
    if username:
        orders = orders.filter(user__username=username)
    return orders
