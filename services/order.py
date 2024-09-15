from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list,
        username: str,
        date: str = None,
) -> None:

    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket.get("movie_session"),
                order=order,
                row=ticket.get("row"),
                seat=ticket.get("seat")
            )


def get_orders(username: str = None) -> QuerySet:
    order = Order.objects.all()
    if username:
        order = order.filter(user__username=username)
    return order
