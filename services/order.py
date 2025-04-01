from datetime import datetime
from typing import Optional
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save(update_fields=["created_at"])

        ticket_objects = [
            Ticket(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                )
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(ticket_objects)
    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
