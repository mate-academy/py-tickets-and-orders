import datetime

from db.models import Order, User, Ticket
from django.db import transaction
from django.db.models import QuerySet


def create_order(
    tickets: list[dict],
    username: str,
    date: datetime.datetime | None = None,
) -> None:
    with transaction.atomic():
        order = Order()
        order.user = User.objects.get(username=username)
        order.save()
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        return Order.objects.filter(
            user__username=username
        )
    return Order.objects.all()
