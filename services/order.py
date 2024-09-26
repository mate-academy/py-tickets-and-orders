from __future__ import annotations

from django.db.models import QuerySet
from django.db import transaction

from db.models import Order, Ticket
from services.user import get_user_by_name


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:

    user = get_user_by_name(username)

    new_order = Order.objects.create(
        user=user
    )
    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket.get("movie_session"),
            order_id=new_order.id,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )


def get_orders(username: str | None = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        user = get_user_by_name(username)
        orders = orders.filter(user=user)
    return orders
