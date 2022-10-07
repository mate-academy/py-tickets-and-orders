from typing import List

from django.db import transaction

import init_django_orm  # noqa: F401

from db.models import Order, Ticket, MovieSession, User


def create_order(tickets: List[dict], username: str, date=None) -> Order:

    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user, created_at=date)
        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(id=ticket_data["movie_session"])
            Ticket.objects.create(order=order, movie_session=movie_session,
                                  row=ticket_data["row"], seat=ticket_data["seat"])
    return order

def get_orders(username=None):
    if username:
        return MovieSession.objects.get(username=username)
    return MovieSession.objects.all()

