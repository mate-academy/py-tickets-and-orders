from datetime import datetime
from typing import Optional

from django.db.models import QuerySet
from django.db import transaction

from services.user import get_or_create_user
from services.movie_session import get_movie_session_by_id
from db.models import Ticket, Order


def create_order(
    tickets: list[dict], username: str, date: Optional[datetime] = None
) -> list[Ticket]:
    with transaction.atomic():
        user = get_or_create_user(username)
        if date:
            order = Order.objects.create(user=user, created_at=date)
        else:
            order = Order.objects.create(user=user)

        result = []
        for ticket_data in tickets:
            result.append(
                Ticket(
                    order=order,
                    movie_session=get_movie_session_by_id(
                        ticket_data.pop("movie_session")
                    ),
                    **ticket_data
                )
            )
        [ticket.save() for ticket in result]

    return result


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
