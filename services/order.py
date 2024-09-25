from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet

from db.models import User
from db.models import Order
from db.models import MovieSession
from db.models import Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user,)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            Ticket.objects.create(order=order,
                                  movie_session=movie_session,
                                  row=ticket["row"],
                                  seat=ticket["seat"],)


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
