from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Ticket, Order, MovieSession
import datetime


def create_order(tickets: list, username: str, date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)

        if date:
            order_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            order = Order.objects.create(user=user, created_at=order_date)
        else:
            order = Order.objects.create(user=user)

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket["movie_session"]
            )

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str = None) -> list:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
