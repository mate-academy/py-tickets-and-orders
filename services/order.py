from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(
        user=(get_object_or_404(get_user_model(), username=username))
    )
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=get_object_or_404(
                MovieSession,
                pk=ticket["movie_session"]
            ),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
