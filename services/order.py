from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User
from services.movie_session import get_movie_session_by_id


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )

        if date:
            order.created_at = date

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=get_movie_session_by_id(ticket["movie_session"]),
                order_id=order.id
            )

        order.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)
    return orders
