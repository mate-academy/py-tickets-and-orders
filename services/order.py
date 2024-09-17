from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import Ticket, Order


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    current_user = get_object_or_404(get_user_model(), username=username)
    new_order = Order.objects.create(user=current_user)
    if date:
        new_order.created_at = date
    for ticket_data in tickets:
        Ticket.objects.create(
            order=new_order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
        new_order.save()
    return new_order


def get_orders(
        username: Optional[str] = None
) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
