from django.contrib.auth import get_user_model
from django.db import transaction
from datetime import datetime
from typing import List, Dict
from django.db.models import QuerySet
from db.models import Ticket, Order


@transaction.atomic
def create_order(tickets: List[Dict],
                 username: str,
                 date: datetime = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)
    return queryset
