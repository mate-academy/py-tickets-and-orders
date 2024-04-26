from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str = None,
        date: str = None
) -> Order:
    order = Order(
        user=get_user_model().objects.get(username=username),
    )
    with transaction.atomic():
        order.save()
        if date:
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = date
            order.save()
        tickets = [
            Ticket(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order
            ) for ticket in tickets
        ]
        Ticket.objects.bulk_create(tickets)

    return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(
            user=get_user_model().objects.get(username=username)
        )
    return orders
