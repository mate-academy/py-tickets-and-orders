from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[datetime] = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )
        return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    query_set = Order.objects.all()
    if username:
        query_set = query_set.filter(user__username=username)

    return query_set
