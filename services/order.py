from datetime import datetime
from typing import Optional

from django.db import transaction

from db.models import Order, User, Ticket


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[datetime] = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        kwargs = {"user": user}
        if date:
            kwargs.update({"created_at": date})
        order = Order.objects.create(**kwargs)

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(
    username: Optional[str] = None
):
    if username:
        return User.objects.get(username=username).order_set.all()
    return Order.objects.all()
