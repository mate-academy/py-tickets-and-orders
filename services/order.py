from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


def create_order(
    tickets: list[dict], username: str, date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = ticket["movie_session"]

            Ticket.objects.create(
                movie_session_id=movie_session,
                row=ticket["row"],
                seat=ticket["seat"],
                order=order,
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.order_by("-user")

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
