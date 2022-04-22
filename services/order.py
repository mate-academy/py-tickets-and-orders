from typing import List

from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Ticket, Order, MovieSession


def create_order(
        tickets: List[dict],
        username: str,
        date=None
):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            if ticket["movie_session"]:
                movie = MovieSession.objects.get(
                    pk=ticket["movie_session"]
                )
                ticket["movie_session"] = movie

            Ticket.objects.create(order=order, **ticket)


def get_orders(username: str = None):
    order = Order.objects.all()

    if username:
        order = order.filter(user__username=username)
    return order
