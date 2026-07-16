from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from typing import List
import datetime


@transaction.atomic
def create_order(
    tickets: List[dict],
    username: str,
    date: str | None = None,
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        created_at = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.created_at = created_at
        order.save(update_fields=["created_at"])

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username is None:
        return Order.objects.all()
    return Order.objects.filter(user__username=username)
