from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        tickets = [
            Ticket(
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session_id=ticket.get("movie_session"),
                order=order
            )
            for ticket in tickets
        ]

        for ticket in tickets:
            ticket.full_clean()

        Ticket.objects.bulk_create(tickets)

        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    query_set = Order.objects.all()

    if username:
        query_set = query_set.filter(user__username=username)

    return query_set
