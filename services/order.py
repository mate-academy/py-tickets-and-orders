from typing import List, Dict

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: List[Dict[str, int]],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            row = ticket_data["row"]
            seat = ticket_data["seat"]
            movie_session_id = ticket_data["movie_session"]

            Ticket.objects.create(
                movie_session_id=movie_session_id,
                order=order,
                row=row,
                seat=seat,
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
