from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order | str:
    with transaction.atomic():
        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return "There no user with such username"
        order = Order.objects.create(
            user=user,
        )

        if date:
            order.created_at = date

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
        order.save()
        return order


def get_orders(username: str = None) -> QuerySet[Order] | None:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
