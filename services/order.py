from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )


def get_orders(username: str = None) -> list[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
