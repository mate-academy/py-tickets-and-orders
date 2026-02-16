from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
import datetime


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        row = ticket.get("row")
        seat = ticket.get("seat")
        movie_session = ticket.get("movie_session")
        Ticket.objects.create(
            row=row,
            seat=seat,
            movie_session_id=movie_session,
            order=order
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    queries = Order.objects.all()
    if username:
        queries = queries.filter(user__username=username)
    return queries
