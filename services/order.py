from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket
from django.contrib.auth.models import User


def create_order(
        tickets: list,
        username: str,
        date: Optional[str] = None
) -> Order | None:
    try:
        user = get_user_model().objects.get(username=username)
        with transaction.atomic():
            order = Order.objects.create(user=user, created_at=date)
            for ticket_data in tickets:
                Ticket.objects.create(
                    movie_session_id=ticket_data["movie_session"],
                    order=order,
                    row=ticket_data["row"],
                    seat=ticket_data["seat"]
                )
        return order
    except User.DoesNotExist:
        return None


def get_orders(username: Optional[str] = None) -> Order:
    if username:
        user = get_user_model().objects.get(username=username)
        orders = Order.objects.filter(user=user)
    else:
        orders = Order.objects.all()
    return orders
