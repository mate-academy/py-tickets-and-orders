from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[datetime] = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            order.created_at = date
            order.save()

        movie_session_ids = {ticket["movie_session"] for ticket in tickets}

        existing_sessions = set(
            MovieSession.objects.filter(id__in=movie_session_ids).values_list(
                "id", flat=True
            )
        )

        if movie_session_ids - existing_sessions:
            raise ObjectDoesNotExist

        Ticket.objects.bulk_create([
            Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ])


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
