import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list,
        username: str,
        date: datetime = None
) -> tuple[Order, list[Ticket]]:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        created_tickets = []

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            created_tickets.append(
                Ticket.objects.create(
                    order=order,
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session=movie_session
                )
            )

    return order, created_tickets


def get_orders(username: str = None) -> QuerySet[Order] | None:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
