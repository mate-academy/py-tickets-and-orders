from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order
from db.models import Ticket
from db.models import MovieSession


def create_order(tickets: list, username: str, date: str = None) -> Order:
    user_from_db = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user_from_db)

        if date:
            order.created_at = date

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                order=order,
                movie_session=MovieSession.objects.get(
                    id=ticket.get("movie_session"))
            )
        order.save()
    return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
