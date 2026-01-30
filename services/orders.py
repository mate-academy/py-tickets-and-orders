from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    *,
    tickets: list[dict[str, Any]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user_model = get_user_model()
    user = user_model.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date is not None:
        dt = parse_datetime(date)
        if dt is not None:
            order.created_at = dt
            order.save(update_fields=["created_at"])

    ticket_objects = []
    for ticket in tickets:
        ticket_objects.append(
            Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )
        )

    Ticket.objects.bulk_create(ticket_objects)
    return order


def get_orders(*, username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
