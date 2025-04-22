from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from typing import List, Optional, Dict, Any
import datetime

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
    tickets: List[Dict[str, Any]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    """Create an order with associated tickets for a user."""
    user = get_user_model().objects.get(username=username)
    created_at = (
        datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        if date
        else datetime.datetime.now()
    )
    order = Order.objects.create(
        user=user,
        created_at=created_at,
    )
    for ticket_data in tickets:
        session = MovieSession.objects.get(id=ticket_data["movie_session"])
        Ticket.objects.create(
            movie_session=session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
    return order


def get_orders(
    username: Optional[str] = None,
) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
