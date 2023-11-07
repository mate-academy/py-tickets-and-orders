import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:

    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = datetime.datetime.strptime(
                date,
                "%Y-%m-%d %H:%M"
            )

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )

        order.save()
        return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(
            user__username=username
        )

    return Order.objects.all()
