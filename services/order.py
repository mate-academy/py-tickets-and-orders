from typing import Optional, List, Dict

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None,
) -> None:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        ticket = Ticket(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order,
        )
        ticket.full_clean()
        ticket.save()


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
