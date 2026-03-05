from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> None:
    user = get_user_model().objects.get(username=username)

    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order.objects.create(user=user, created_at=created_at)
    else:
        order = Order.objects.create(user=user)

    for ticket in tickets:
        ticket["movie_session_id"] = ticket.pop("movie_session")
        Ticket.objects.create(order=order, **ticket)


def get_orders(username: str = None) -> QuerySet[Order]:
    orders_query_set = Order.objects.all()
    if username:
        return orders_query_set.filter(user__username=username)
    return orders_query_set
