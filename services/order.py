from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
