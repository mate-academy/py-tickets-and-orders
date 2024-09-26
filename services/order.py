from datetime import datetime

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic()
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime | None = None) -> None:

    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(movie_session_id=ticket.get("movie_session"),
                              order=order,
                              row=ticket.get("row"),
                              seat=ticket.get("seat"))


@transaction.atomic()
def get_orders(username: str | None = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
