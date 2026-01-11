from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        row, seat, movie_session_id = ticket.values()
        Ticket.objects.create(
            order=order,
            row=row,
            seat=seat,
            movie_session_id=movie_session_id
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    quer = Order.objects.all()
    if username:
        quer = quer.filter(user__username=username)
    return quer
