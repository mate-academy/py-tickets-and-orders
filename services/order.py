from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    the_user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        the_order = Order.objects.create(user=the_user)
        if date:
            the_order.created_at = date
            the_order.save()
        [
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=the_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]


def get_orders(username: str = "") -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
