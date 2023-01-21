from typing import List
from django.db.models import QuerySet
from db.models import Ticket, User, Order
from django.db import transaction
from datetime import datetime


def create_order(tickets: List[dict],
                 username: str,
                 date: datetime = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username).values_list()
    return Order.objects.all()
