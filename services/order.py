from typing import Optional
from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, User, Ticket


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None
) -> None:
    with transaction.atomic():
        if username:
            new_order = Order.objects.create(
                user=get_user_model().objects.get(username=username)
            )
        if date:
            new_order.created_at = date

        for ticket in tickets:
            Ticket.objects.create(
                order=new_order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"]
            )
        new_order.save()


def get_orders(username: Optional[str] = None) -> Order:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))
    return Order.objects.all()
