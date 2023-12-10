from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from services.movie_session import get_taken_seats, get_movie_session_by_id


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        movie_session = ticket["movie_session"]
        seat_data = dict(list(ticket.items())[:2])

        if seat_data not in get_taken_seats(movie_session):
            Ticket.objects.create(
                movie_session=get_movie_session_by_id(movie_session),
                order=order,
                **seat_data
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
