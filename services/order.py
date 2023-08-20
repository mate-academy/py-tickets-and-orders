from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket, MovieSession


def create_order(tickets: list[dict], username: str, date: datetime = None):
    with transaction.atomic():
        order = Order.objects.create(user=get_user_model().objects.get(username=username))
        if date is not None:
            Order.objects.filter(id=order.id).update(created_at=date)

        Ticket.objects.bulk_create(
            Ticket(
                movie_session=MovieSession.objects.get(id=ticket_data["movie_session"]),
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            ) for ticket_data in tickets
        )

        return order


def get_orders(username: str = None) -> QuerySet:
    order = Order.objects.all()
    if username is not None:
        order = order.filter(user__username=username)
    return order
