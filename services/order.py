from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket

User = get_user_model()


def _parse_order_date(date: datetime | str) -> datetime:
    if isinstance(date, datetime):
        return date

    parsed_date = parse_datetime(date)
    if parsed_date is not None:
        return parsed_date

    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            continue

    raise ValueError("Invalid date format")


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime | str | None = None,
) -> Order:
    user = User.objects.get(username=username)
    parsed_date = _parse_order_date(date) if date is not None else None

    order = Order.objects.create(user=user)

    if parsed_date is not None:
        Order.objects.filter(id=order.id).update(created_at=parsed_date)
        order.refresh_from_db()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
