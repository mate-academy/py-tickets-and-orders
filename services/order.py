import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()
    list_of_ticket = []
    for ticket in tickets:
        movie_session_id = ticket.get("movie_sessions")
        movie_session = Ticket.objects.get(
            id=movie_session_id
        )
        seat = ticket.get("seat")
        row = ticket.get("row")
        create_ticket = Ticket(
            row=row,
            seat=seat,
            movie_session=movie_session,
            order=order
        )
        list_of_ticket.append(create_ticket)
    Ticket.objects.bulk_create(list_of_ticket)

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
