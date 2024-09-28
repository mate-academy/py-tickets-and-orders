from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date

        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        orders = Order.objects.filter(user=user)
    else:
        orders = Order.objects.all()

    return orders
