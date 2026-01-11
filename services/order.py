import datetime

from db.models import Order
from django.db import transaction
from typing import List
from db.models import MovieSession, Ticket
from db.models import User


@transaction.atomic
def create_order(
        tickets: List[dict],
        username: str,
        date: datetime = None
) -> None:
    user, created = User.objects.get_or_create(username=username)
    order, created = Order.objects.get_or_create(user=user)
    if date is not None:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")
        movie_session = MovieSession.objects.get(pk=1)
        ticket, created = Ticket.objects.get_or_create(
            row=row,
            seat=seat,
            movie_session=movie_session,
            order=order
        )
        ticket.order = order
        ticket.save()


def get_orders(username: str = None) -> list:
    if username is not None:
        return Order.objects.filter(
            user__username=username).order_by("created_at"
                                              )
    elif username is None:
        return Order.objects.all().order_by("-created_at")
