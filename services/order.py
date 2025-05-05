from datetime import datetime

from db.models import Order, Ticket, User, MovieSession
from django.db import transaction
from django.db.models import QuerySet


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        new_order = Order.objects.create(
            user=user
        )
        if date:
            new_order.created_at = date
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            new_ticket = Ticket.objects.create(
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"],
                order=new_order
            )

        new_order.save()


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
