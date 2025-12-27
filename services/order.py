from typing import List, Dict, Optional
from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: List[Dict],
        username: str,
        date: datetime = None
) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with username {username} doesn't exist.")

    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        movie_session_id = ticket_data.get("movie_session")
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")

        if not all([movie_session_id, row, seat]):
            raise ValueError(
                "Each ticket must have 'movie_session',"
                "'row', and 'seat' fields."
            )

        try:
            movie_session = MovieSession.objects.get(id=movie_session_id)
        except MovieSession.DoesNotExist:
            raise ValueError(
                f"Movie session with id {movie_session_id} doesn't exist."
            )

        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat
        )

    return order


def get_orders(
        username: Optional[str] = None
) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
