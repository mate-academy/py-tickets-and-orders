import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list[dict], username: str,
                 date: datetime.datetime = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    order.save()

    ticket_objects = [
        Ticket(
            order=order,
            movie_session=MovieSession.objects.
            get(id=ticket["movie_session"]),
            row=ticket["row"],
            seat=ticket["seat"]
        ) for ticket in tickets
    ]

    Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
