import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet, Q

from db.models import Order


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: datetime.date = None
) -> None:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        order.tickets.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Q()
    if username:
        queryset &= Q(user__username=username)

    return Order.objects.filter(queryset)
