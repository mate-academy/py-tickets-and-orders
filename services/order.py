from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None
) -> None:
    with transaction.atomic():
        user: User = get_user_model()
        current_user = user.objects.get(username=username)
        current_order = Order.objects.create(user=current_user)

        if date is not None:
            current_order.created_at = date
            current_order.save()

        for ticket in tickets:
            ticket["movie_session_id"] = ticket["movie_session"]
            del ticket["movie_session"]

            Ticket.objects.create(
                order=current_order,
                **ticket
            )


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.select_related("user").filter(
            user__username=username
        )

    return queryset
