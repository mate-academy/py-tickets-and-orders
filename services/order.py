import datetime
from typing import Dict, List, Optional
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    """
    Create an order for a given user and tickets.
    If date is provided, set created_at manually.
    Transaction ensures all-or-nothing execution.
    """
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        parsed = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.created_at = parsed
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    """
    Return all orders, optionally filtered by username.
    Ordered newest to oldest by default.
    """
    qs = Order.objects.select_related("user")
    if username:
        qs = qs.filter(user__username=username)
    return qs
