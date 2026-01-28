from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: datetime | None = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str | None = None) -> list:
    return Order.objects.filter(
        user__username=username
    ) if username else Order.objects.all()
