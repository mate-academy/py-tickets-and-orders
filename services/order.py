from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, MovieSession, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:

    with transaction.atomic():

        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(row=ticket["row"],
                                  seat=ticket["seat"],
                                  movie_session=movie_session,
                                  order=order)
        if date:
            order.created_at = date
            order.save()


def get_orders(username: str = None) -> QuerySet:

    if username:
        user = User.objects.get(username=username)
        return user.orders.all()
    return Order.objects.all()
