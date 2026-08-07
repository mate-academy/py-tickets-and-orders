from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket
from services.user import get_user_by_username


@transaction.atomic
def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: str | datetime = None,
) -> Order:
    user = get_user_by_username(username=username)
    created_at = None

    if date is not None:
        created_at = parse_datetime(date) if isinstance(date, str) else date

        if not isinstance(created_at, datetime):
            raise ValueError("date must be a valid datetime")

    order = Order.objects.create(
        user=user,
        created_at=created_at,
    )

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username is not None:
        orders = orders.filter(user__username=username)

    return orders
