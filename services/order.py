from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            order.created_at = date
            order.save()

        new_tickets = [
            Ticket(
                movie_session=MovieSession.objects.get(
                    pk=ticket["movie_session"]
                ),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(new_tickets)
        return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
