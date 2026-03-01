from typing import List

from django.db import transaction
from db.models import Order, Ticket
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


def create_order(tickets: List[dict],
                 username: str,
                 date: [str] = None) -> None:

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValidationError("User does not exist")

    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        created_at = datetime.now()

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=created_at)
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str) -> List[Order]:

    """
    Retrieves a list of orders, optionally filtered by username.

    Args:
        username (str): The username to filter orders by (optional).

    Returns:
        QuerySet: A Django QuerySet of orders.
    """
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
