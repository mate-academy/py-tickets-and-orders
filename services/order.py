from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


def get_orders(username: str = None) -> QuerySet[Order]:
    query_set = Order.objects.all()

    if username:
        query_set = query_set.filter(user__username=username)

    return query_set


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

        if date:
            order.created_at = date
            order.save()

        tickets_list = [
            Ticket(
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session=MovieSession.objects.get(
                    pk=ticket.get("movie_session")
                ),
                order=order,
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(tickets_list)
