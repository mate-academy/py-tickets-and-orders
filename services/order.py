from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket
from datetime import datetime
from django.db import transaction


def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=get_user_model().objects.get(
                username=username
            )
        )
        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=new_order,
                seat=ticket["seat"],
                row=ticket["row"],
                movie_session_id=ticket["movie_session"]
            )
        return new_order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return get_user_model().objects.get(username=username).orders.all()
    return Order.objects.all()
