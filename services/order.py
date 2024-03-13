from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            row = ticket["row"]
            seat = ticket["seat"]
            movie_session = ticket["movie_session"]

            Ticket.objects.create(
                row=row,
                seat=seat,
                movie_session_id=movie_session,
                order=order
            )
    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
