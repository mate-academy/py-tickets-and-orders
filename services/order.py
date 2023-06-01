from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    order_obj = Order.objects.create(
        user=User.objects.get(username=username)
    )

    if date:
        order_obj.created_at = date
        order_obj.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket.get("movie_session"),
            order=order_obj,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )
    return order_obj


def get_orders(username: Optional[str] = None) -> QuerySet:
    query_set = Order.objects.all()
    if username:
        query_set = query_set.filter(user__username=username)
    return query_set
