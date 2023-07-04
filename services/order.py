from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None) -> None:

    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        for ticket_data in tickets:
            Ticket.objects.create(
                order_id=order.id,
                movie_session_id=ticket_data["movie_session"],
                row=ticket_data["row"],
                seat=ticket_data["seat"])

        order.save()


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
