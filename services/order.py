from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from typing import Optional
from django.shortcuts import get_object_or_404


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:
    user = get_object_or_404(get_user_model(), username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(
        username: Optional[str] = None
) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = Order.objects.filter(user__username=username)
    return orders
