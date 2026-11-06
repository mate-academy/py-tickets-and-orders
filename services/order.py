import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None,
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
        )

    return order


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)
    return queryset

