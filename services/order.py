import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from typing import Optional

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime.datetime] = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)

        if date:
            new_order.created_at = date
            new_order.save()

        for ticket_data in tickets:
            movie_session_id = ticket_data.pop("movie_session")
            Ticket.objects.create(
                order=new_order,
                movie_session_id=movie_session_id,
                **ticket_data
            )


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
