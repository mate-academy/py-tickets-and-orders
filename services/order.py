from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[str] = None) -> None:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=get_user_model().objects.get(username=username))
        if date:
            new_order.created_at = date
            new_order.save()
        for detail in tickets:
            Ticket.objects.create(order=new_order,
                                  movie_session_id=detail["movie_session"],
                                  row=detail["row"],
                                  seat=detail["seat"])


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
