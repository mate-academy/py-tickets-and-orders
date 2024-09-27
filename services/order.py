from django.contrib.auth import get_user_model

from db.models import Order, Ticket, MovieSession
from django.db import transaction
from typing import List


def create_order(
        tickets: dict,
        username: str,
        date: str = None
) -> None:

    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket["movie_session"]
            )

            Ticket.objects.create(row=ticket["row"],
                                  seat=ticket["seat"],
                                  movie_session=movie_session,
                                  order=order)


def get_orders(username: str = None) -> List[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
