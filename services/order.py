from typing import Optional, List

from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: List[dict],
    username: str,
    date: Optional[str] = None,
) -> Ticket:
    find_user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user_id=find_user.id)

    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        new_ticket = Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order_id=order.id
        )

    return new_ticket


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
