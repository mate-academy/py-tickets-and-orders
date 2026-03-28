from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        for ticket in tickets:
            row, seat, movie_session_id = ticket.values()
            movie_session = MovieSession.objects.get(id=movie_session_id)
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=row,
                seat=seat
            )

        if date:
            order.created_at = date
            order.save()

        return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders = Order.objects.select_related("user")
    if username:
        orders = orders.filter(user__username=username)

    return orders
