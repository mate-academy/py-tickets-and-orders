from datetime import datetime

from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from django.db import transaction
from django.contrib.auth import get_user_model


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None
                 ) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username))

        if date:
            order.created_at = date
            order.save()

        Ticket.objects.bulk_create([Ticket(
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        ) for ticket in tickets])


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = Order.objects.filter(user__username=username)
    return orders
