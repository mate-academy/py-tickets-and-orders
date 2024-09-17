from __future__ import annotations
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from typing import List
import datetime
from db.models import Order, Ticket


def create_order(tickets: List[dict], username: str,
                 date: datetime = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(movie_session_id=ticket["movie_session"],
                                  order=order, row=ticket["row"],
                                  seat=ticket["seat"])


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
