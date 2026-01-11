from typing import Optional, List, Dict
from django.db import transaction
from django.contrib.auth import get_user_model

from db.models import Order, Ticket

User = get_user_model()


def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None
) -> Order:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = (
            Order.objects.create(user=user, created_at=date)
            if date
            else Order.objects.create(user=user)
        )
        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket_data["movie_session"],
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
    return order


def get_orders(username: Optional[str] = None) -> Order.objects.__class__:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
