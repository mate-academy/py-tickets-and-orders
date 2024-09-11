from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:
    user = get_user_model().objects.get(username=username)
    new_data = {}
    if date:
        new_data["created_at"] = date

    with transaction.atomic():
        order = Order.objects.create(user=user)
        Order.objects.filter(id=order.id).update(**new_data)
        for ticket in tickets:
            ticket["movie_session_id"] = ticket["movie_session"]
            del ticket["movie_session"]
            Ticket.objects.create(order=order, **ticket)


def get_orders(username: str | None = None) -> QuerySet:
    query = Order.objects.all()

    if username:
        query = query.filter(user__username=username)

    return query
