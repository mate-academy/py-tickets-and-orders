from django.db import transaction
from typing import Optional
from datetime import datetime

from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[datetime] = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            ticket = Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )
            order.ticket_set.add(ticket)


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
