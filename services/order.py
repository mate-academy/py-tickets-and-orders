import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> list[Ticket]:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        (
            Order.objects
            .filter(pk=order.pk)
            .update(
                created_at=datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            )
        )
    return [
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        ) for ticket in tickets]


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    query_set = Order.objects.all()
    if username:
        query_set = (
            query_set.select_related("user")
            .filter(user__username=username)
        )
    return query_set
