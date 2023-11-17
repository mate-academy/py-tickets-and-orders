from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(
            username=username
        )
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            row = ticket.get("row")
            seat = ticket.get("seat")
            movie_session = ticket.get("movie_session")

            Ticket.objects.create(
                order_id=order.id,
                row=row,
                seat=seat,
                movie_session_id=movie_session
            )


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
