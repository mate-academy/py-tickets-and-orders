from django.db import transaction
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = User.objects.get(username=username)
    date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=date)

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
            )

        return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        user = User.objects.get(username=username)
        queryset = queryset.filter(user=user)

    return queryset
