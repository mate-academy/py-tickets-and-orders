import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
    tickets: list[dict], username: str, date: datetime = None
) -> Order:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(
            user=user,
        )
        if date:
            order.created_at = date

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"],
                order=order,
            )
        order.save()
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
