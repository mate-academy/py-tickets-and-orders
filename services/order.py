from datetime import datetime

from django.db.models import QuerySet

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            order.created_at = date
        order.save()
        for ticket in tickets:
            row, seat, session_id = ticket.values()
            Ticket.objects.create(
                order=order,
                row=row,
                seat=seat,
                movie_session_id=session_id
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
