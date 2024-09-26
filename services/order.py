from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket
from django.utils import timezone
from typing import Optional


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    if date is None:
        date = timezone.now()
    order = Order.objects.create(user=user, created_at=date)
    for ticket_data in tickets:
        row = ticket_data["row"]
        seat = ticket_data["seat"]
        movie_session_id = ticket_data["movie_session"]
        Ticket.objects.create(
            order=order,
            movie_session_id=movie_session_id,
            row=row,
            seat=seat,
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
