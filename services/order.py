from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket

from services.user import get_or_create_user


def create_order(
    tickets: list[dict], username: str, date: Optional[datetime] = None
) -> list[Ticket]:
    with transaction.atomic():
        user = get_or_create_user(username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        result = []
        for ticket_data in tickets:
            movie_session_id = ticket_data.pop("movie_session")
            result.append(
                Ticket(
                    order=order,
                    movie_session_id=movie_session_id,
                    **ticket_data
                )
            )
        Ticket.objects.bulk_create(result)

    return result


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
