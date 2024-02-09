from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket.pop("movie_session"),
                **ticket
            )

        order.save()
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username__icontains=username)

    return Order.objects.all()
