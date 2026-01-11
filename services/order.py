from django.db import transaction
from django.db.models import Model

from db.models import Ticket, Order, User, MovieSession

from django.db.models.query import QuerySet

from datetime import datetime


def create_order(tickets: list, username: str, date: datetime = None) -> Model:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]),
                row=ticket["row"],
                seat=ticket["seat"]
            )
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
