from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(
                username=username
            ),
        )
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie_session
            )

        if date:
            Order.objects.filter(
                pk=order.pk
            ).update(
                created_at=datetime.strptime(
                    date, "%Y-%m-%d %H:%M"
                )
            )
    return order


def get_orders(
        username: str = None,
) -> QuerySet:
    if username:
        orders = Order.objects.filter(user__username=username)
        return orders
    return Order.objects.all()
