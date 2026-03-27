from datetime import datetime

from django.db.models import QuerySet
from db.models import Order, Ticket, User, MovieSession
from django.db import transaction


def create_order(
        tickets: list[Ticket],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(
            user=user
        )
        if date is not None:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
