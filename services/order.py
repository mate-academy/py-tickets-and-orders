import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:

    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.datetime.strptime(
            date, "%Y-%m-%d %H:%M"
        )
        order.save()
    for ticket in tickets:
        row = ticket["row"]
        seat = ticket["seat"]
        movie_session = MovieSession.objects.get(
            id=ticket["movie_session"]
        )
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=row,
            seat=seat
        )

    return order


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        queryset = queryset.filter(user=user)
    return queryset
