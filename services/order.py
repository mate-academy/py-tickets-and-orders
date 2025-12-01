from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime

from db.models import Order, Ticket, MovieSession


@transaction.atomic()
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    ticket_objects = []
    for ticket in tickets:
        movie_session_id = ticket["movie_session"]
        movie_session = MovieSession.objects.get(id=movie_session_id)
        ticket_objects.append(Ticket(
            order=order,
            movie_session=movie_session,
            row=ticket["row"],
            seat=ticket["seat"]
        ))

    Ticket.objects.bulk_create(ticket_objects)


def get_orders(
        username: str = None,
) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
