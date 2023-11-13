from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.db.models.functions import datetime

from db.models import Order, Ticket


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:

    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    for ticket_date in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_date["movie_session"],
            row=ticket_date["row"],
            seat=ticket_date["seat"],
        )
        # **ticket_date why this is not working, because movie_session
        # in ticket_date and I need movie_session_id
    order.save()


def get_orders(username: str | None = None) -> QuerySet:

    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
