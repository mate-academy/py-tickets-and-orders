from datetime import datetime
from typing import Any

from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket, User


def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value

    parsed = parse_datetime(value)
    if parsed is not None:
        return parsed

    return datetime.strptime(value, "%Y-%m-%d %H:%M")


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        created_at = _parse_datetime(date)
        Order.objects.filter(id=order.id).update(created_at=created_at)
        order.refresh_from_db()

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)
    return queryset
