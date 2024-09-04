from django.contrib.auth import get_user_model

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, MovieSession, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            MovieSession.objects.get(pk=ticket["movie_session"])
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )

        return order


def get_orders(username: str | None = None) -> QuerySet:
    filters = {}
    if username:
        filters["user__username"] = username
    return Order.objects.filter(**filters)
