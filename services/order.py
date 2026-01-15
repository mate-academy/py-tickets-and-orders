from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime | None = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(
            user=get_user_model().objects.get(username=username))
    return queryset
