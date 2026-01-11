from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: Optional[str] = None
) -> Order | None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
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
    return order


def get_orders(username: Optional[str] = None) -> Order:
    if username:
        user = get_user_model().objects.get(username=username)
        orders = Order.objects.filter(user=user)
    else:
        orders = Order.objects.all()
    return orders
