from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
