from datetime import datetime

from db.models import Order, Ticket, MovieSession
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:

    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        for ticket in tickets:
            if ticket["movie_session"]:
                movie_session = MovieSession.objects.get(
                    id=ticket["movie_session"]
                )
                ticket["movie_session"] = movie_session

            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=ticket["movie_session"]
            )

        if date:
            order.created_at = date
        order.save()
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
