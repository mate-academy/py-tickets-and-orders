from typing import List

from django.db import transaction

import init_django_orm  # noqa: F401

from db.models import Order, Ticket, MovieSession, User


def create_order(tickets: List[dict], username: str, date=None) -> Order:

    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user, created_at=date)

        if date:
            order.created_at = date
            order.save()
        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"])
            Ticket.objects.create(order=order,
                                  movie_session=movie_session,
                                  row=ticket_data["row"],
                                  seat=ticket_data["seat"])

        return order


def get_orders(username=None):
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all().order_by("-user")
