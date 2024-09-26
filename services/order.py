from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(
                date, "%Y-%m-%d %H:%M"
            )
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order,
            )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
