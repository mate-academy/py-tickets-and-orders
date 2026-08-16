from datetime import datetime
from typing import Optional

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[datetime] = None,
) -> None:
    user_instance = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user_instance)
    if date:
        order.created_at = date
    order.save()
    for ticket in tickets:
        m_session = MovieSession.objects.get(
            id=ticket.get("movie_session")
        )
        Ticket.objects.create(
            movie_session=m_session,
            order=order,
            row=ticket.get("row"),
            seat=ticket.get("seat"),
        )


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
