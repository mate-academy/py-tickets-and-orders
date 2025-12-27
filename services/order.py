from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None
) -> Order:
    user, _ = User.objects.get_or_create(username=username)
    order, _ = Order.objects.get_or_create(user=user)
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


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
