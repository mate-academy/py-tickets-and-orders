from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from django.db.models import QuerySet

from db.models import Order, Ticket


@atomic
def create_order(
    tickets: list[dict], username: str, date: Optional[datetime] = None
) -> None:
    if tickets:
        order_to_create = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

        if date:
            order_to_create.created_at = date
            order_to_create.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket.get("movie_session"),
                order=order_to_create,
                row=ticket.get("row"),
                seat=ticket.get("seat"),
            )


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return get_user_model().objects.get(username=username).orders.all()
    return Order.objects.all()
