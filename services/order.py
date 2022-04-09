from typing import List

from django.db import transaction

from db.models import Ticket, User, Order, MovieSession


def create_order(
        tickets: List[dict],
        username: str,
        date=None
):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user)

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
    queryset = Order.objects.all()

    if username:
        queryset.filter(user__username=username)
    return queryset
