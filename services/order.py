from typing import List, Optional
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from db.models import Order, Ticket, MovieSession, User


def create_order(
    tickets: List[dict],
    username: str,
    date: Optional[str] = None,
) -> Order:
    """
    Create an order for a user, with tickets.
    Ensures atomicity for the entire operation.
    """
    try:
        user = get_object_or_404(User, username=username)
    except ObjectDoesNotExist:
        raise ValueError(
            f"User with username '{username}' does not exist.")

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=date)
        for ticket_data in tickets:
            movie_session = get_object_or_404(
                MovieSession, id=ticket_data["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
            )
    return order


def get_orders(username: Optional[str] = None) -> List[Order]:
    """
    Retrieve all orders, optionally filtered by username.
    """
    if username:
        user = get_object_or_404(User, username=username)
        return list(Order.objects.filter(user=user))
    return list(Order.objects.all())
