from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import Order, Ticket


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

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )


def get_orders(username: Optional[str] = None) -> QuerySet:
    query_set = Order.objects.all()

    if username:
        query_set = query_set.filter(user__username=username)

    return query_set
