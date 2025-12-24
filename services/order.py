from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.datetime_safe import datetime

from db.models import Order, Ticket, MovieSession


def create_order(tickets: list, username: str, date: datetime = None) -> Order:

    with transaction.atomic():
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValueError(
                f"User with username '{username}' does not exist."
            )

        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()

        create_tickets = [
            Ticket(
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session=MovieSession.objects.get(
                    id=ticket.get("movie_session")
                ),
                order=order
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(create_tickets)

    return order


def get_orders(username: str = None) -> list:
    if username:
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValueError(
                f"User with username '{username}' does not exist."
            )
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
