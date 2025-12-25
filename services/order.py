from datetime import datetime
from typing import Optional

from django.db import transaction

from db.models import Order, Ticket, User


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None
) -> None:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        row = ticket_data["row"]
        seat = ticket_data["seat"]
        movie_session_id = ticket_data["movie_session"]

        Ticket.objects.create(
            row=row, seat=seat, movie_session_id=movie_session_id, order=order
        )


def get_orders(username: str = None) -> Order:
    if username:
        user = User.objects.get(username=username)
        orders = Order.objects.filter(user=user)
        return orders
    orders = Order.objects.all()
    return orders
