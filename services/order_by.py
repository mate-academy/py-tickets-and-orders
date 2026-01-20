from datetime import datetime

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(tickets: list[dict], username: str, date: datetime) -> list[dict]:
    with transaction.atomic():
        order = Order.objects.create(username=username, created_at=date)
        for ticket in tickets:
            Ticket.objects.create(row=ticket["row"],
                              seat=ticket["seat"],
                              movie_session=ticket["movie_session"],
                              order=order)


def get_orders(username: str = None) -> QuerySet[User]:
    if username:
        return User.objects.filter(username=username)
    if username is None:
        return User.objects.all()
