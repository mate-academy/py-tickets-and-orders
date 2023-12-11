from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order
from services.movie_session import get_movie_session_by_id, get_taken_seats


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        movie_session = ticket["movie_session"]
        row_seat_data = dict(list(ticket.items())[:2])

        if row_seat_data not in get_taken_seats(movie_session):
            Ticket.objects.create(
                movie_session=get_movie_session_by_id(movie_session),
                order=order,
                **row_seat_data
            )


def get_orders(
        username: str = None
) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = Order.objects.filter(user__username=username)

    return queryset
