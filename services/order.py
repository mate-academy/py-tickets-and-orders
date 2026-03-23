from typing import List
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession
from .user import get_user

@transaction.atomic
def create_order(
    tickets: List[dict],
    username: str,
    date: str | None = None
) -> Order:
    """Create an order and tickets for a user."""
    user = get_user(username=username)  # отримуємо об’єкт User

    if date:
        order = Order.objects.create(user=user, created_at=date)
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session=MovieSession.objects.get(id=ticket_data["movie_session"]),
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    """Get orders optionally filtered by username."""
    if username:
        user = get_user(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
