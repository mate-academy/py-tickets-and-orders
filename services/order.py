import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = get_object_or_404(get_user_model(), username=username)

    order = Order.objects.create(
        user=user
    )

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        movie_session = get_object_or_404(
            MovieSession,
            id=ticket.get("movie_session")
        )

        Ticket.objects.create(
            row=ticket.get("row"),
            seat=ticket.get("seat"),
            movie_session_id=movie_session.id,
            order=order
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(
            user=get_object_or_404(get_user_model(), username=username)
        )
    return Order.objects.all()
