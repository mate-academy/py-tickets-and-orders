from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(
            user=user
        )

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(
        username: str = None
) -> None:
    queryset = Order.objects.all().select_related("user")

    if username:
        user = get_user_model().objects.get(username=username)
        queryset = queryset.filter(user_id=user.id)
    return queryset
