from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        parsed_date = parse_datetime(date)

        if parsed_date is None:
            raise ValueError("Invalid date format")

        order.created_at = parsed_date
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username is not None:
        orders = orders.filter(user__username=username)

    return orders
