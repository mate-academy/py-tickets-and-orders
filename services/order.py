from typing import List, Dict, Optional
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    try:
        user = get_user_model().objects.get(username=username)
    except ValueError:
        raise ValueError(f"User with username '{username}' does not exist")

    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
