import datetime

from typing import Optional

from django.db.models import QuerySet

from django.db import transaction

from db.models import Order, Ticket, User


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None
) -> None:

    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = datetime.datetime.strptime(
                date, "%Y-%m-%d %H:%M"
            )
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"]
            )


def get_orders(username: Optional[str] = None) -> QuerySet:

    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
