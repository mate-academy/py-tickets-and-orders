import datetime
from typing import List

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(tickets: List[dict],
                 username: str,
                 date: datetime.datetime = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(row=ticket["row"],
                              seat=ticket["seat"],
                              movie_session_id=ticket["movie_session"],
                              order=order)


def get_orders(username: str = None) -> QuerySet:
    if not username:
        return Order.objects.all()
    return Order.objects.filter(user__username=username)
