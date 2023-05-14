from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import MovieSession
from db.models import Order
from db.models import Ticket
from db.models import User


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        user_to_add = User.objects.get(username=username)
        new_order = Order.objects.create(user=user_to_add)
        if date:
            new_order.created_at = date
            new_order.save()
        for ticket in tickets:
            Ticket.objects.create(
                seat=ticket["seat"],
                row=ticket["row"],
                movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
                order=new_order
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        user = User.objects.get(username=username)
        queryset = queryset.filter(user=user)
    return queryset
