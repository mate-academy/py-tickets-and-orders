import init_django_orm  # noqa: F401

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction

from db.models import Ticket, Order, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        Ticket.objects.bulk_create(
            [
                Ticket(
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session=MovieSession.objects.get(
                        id=ticket["movie_session"]
                    ),
                    order=order
                ) for ticket in tickets
            ]
        )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all().select_related("user")
    if username:
        orders = orders.filter(user__username__icontains=username)
    return orders
