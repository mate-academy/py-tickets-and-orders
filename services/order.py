from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order


from typing import Optional


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(created_at=date, user_id=user.id)
    for ticket in tickets:
        row, seat, session = ticket.values()
        order.tickets.create(row=row, seat=seat, movie_session_id=session)
    if date:
        order.created_at = date
    order.save()
    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    user = get_user_model()
    if username is not None:
        user = user.objects.get(username=username)
        orders = Order.objects.filter(user=user)
        return orders
    else:
        return Order.objects.all()
