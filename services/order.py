from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict[str, Any]],
    username: str,
    date: str = None,
) -> Order:
    user_model = get_user_model()
    user = user_model.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save(update_fields=["created_at"])

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username is not None:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
