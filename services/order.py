from typing import Optional, Any
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict[str, Any]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order,
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
