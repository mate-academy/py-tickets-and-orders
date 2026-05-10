from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: Optional[str] = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        Order.objects.filter(id=order.id).update(created_at=date)
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"]
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
