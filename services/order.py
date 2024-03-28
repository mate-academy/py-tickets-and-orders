from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction

from db.models import Ticket, Order


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:

    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket.get("movie_session"),
            order_id=order.id,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
