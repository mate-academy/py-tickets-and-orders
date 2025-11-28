import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if isinstance(date, str):
        order.created_at = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
    order.save()
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket.get("movie_session"),
            row=ticket.get("row"),
            seat=ticket.get("seat"),
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)
    return queryset
