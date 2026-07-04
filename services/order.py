from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save()

    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    query_set = Order.objects.all()

    if username:
        query_set = query_set.filter(user__username=username)

    return query_set
