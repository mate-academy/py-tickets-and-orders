from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    for ticket in tickets:
        order.ticket_set.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"]
        )

    if date:
        order.created_at = datetime.strptime(
            date,
            "%Y-%m-%d %H:%M")
    order.save()
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(
            user=get_user_model().objects.get(username=username)
        )
    return Order.objects.all()
