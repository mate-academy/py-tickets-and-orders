from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None,
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order,
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
