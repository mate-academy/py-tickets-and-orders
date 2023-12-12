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
        movie_session = ticket.get("movie_session")
        row = ticket.get("row")
        seat = ticket.get("seat")

        row_seat_data = {
            "movie_session": get_movie_session_by_id(movie_session),
            "order": order,
            "row": row,
            "seat": seat,
        }

        if (row, seat) not in get_taken_seats(movie_session):
            Ticket.objects.create(**row_seat_data)


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = Order.objects.filter(user__username=username)

    return queryset
