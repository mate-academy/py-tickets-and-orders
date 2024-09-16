from datetime import datetime
from typing import List, Optional
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: List[dict],
        username: str,
        date: Optional[str] = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user_id=user.id)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session=MovieSession.objects.get(
                id=ticket.get("movie_session")
            ),
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
