from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = user.orders.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order
        )


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
