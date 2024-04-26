from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str, date:
        datetime = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            ticket_data["movie_session"] = MovieSession.objects.get(
                pk=ticket_data["movie_session"]
            )
            ticket_data["order"] = order
            Ticket.objects.create(**ticket_data)


def get_orders(username: str = None) -> QuerySet:
    order = Order.objects.all()
    if username:
        order = Order.objects.filter(user__username=username)
    return order
