import datetime

from django.db.models import QuerySet

from db.models import Order
from django.db import transaction
from typing import List
from db.models import Ticket
from db.models import User


@transaction.atomic
def create_order(
        tickets: List[dict],
        username: str,
        date: datetime = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")
        ticket, created = Ticket.objects.get_or_create(
            row=row,
            seat=seat,
            movie_session_id=ticket_data["movie_session"],
            order=order
        )
        ticket.order = order
        ticket.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username is not None:
        orders = orders.filter(user__username=username)
    return orders.order_by("-created_at")
