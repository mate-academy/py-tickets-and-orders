from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            order.created_at = date
            order.save()

        movie_session_ids = set(ticket["movie_session"] for ticket in tickets)
        existing_sessions = MovieSession.objects.filter(
            id__in=movie_session_ids
        )

        if len(existing_sessions) != len(movie_session_ids):
            raise ValueError("One or more movie sessions do not exist.")

        new_tickets = [
            Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(new_tickets)
        return order


def get_orders(username: str | None = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
