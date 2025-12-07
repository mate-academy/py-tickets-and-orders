from datetime import datetime
from db.models import Ticket, User, Order, MovieSession
from django.db import transaction


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:
    # ticket = keys: row, seat, movie_session
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date is not None:
            Order.objects.filter(id=order.id).update(created_at=date)
        for ticket in tickets:
            Ticket.objects.create(movie_session=MovieSession.
                                  objects.get(id=ticket["movie_session"]),
                                  order=order,
                                  row=ticket["row"],
                                  seat=ticket["seat"])


def get_orders(username: str = None) -> list[Order]:
    if username is not None:
        return Order.objects.filter(user=User.objects.get(username=username))
    return Order.objects.all()
