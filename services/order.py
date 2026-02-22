from typing import List, Dict, Optional
from django.db import transaction
from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
import datetime

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist.")

    if date:
        try:
            naive_datetime = datetime.datetime.fromisoformat(date)
            created_at = make_aware(naive_datetime)  # <<< ВАЖЛИВО
            order = Order.objects.create(user=user, created_at=created_at)
        except ValueError:
            raise ValueError(
                "Invalid date format. Please use"
                " YYYY-MM-DD HH:MM[:SS[.uuuuuu]][TZ]."
            )
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        movie_session_id = ticket_data.get("movie_session")
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")

        try:
            movie_session = MovieSession.objects.get(id=movie_session_id)
        except MovieSession.DoesNotExist:
            raise ValueError(f"Movie session"
                             f" with id '{movie_session_id}' does not exist.")

        Ticket.objects.create(
            order=order, movie_session=movie_session, row=row, seat=seat
        )

    return order


def get_orders(username: Optional[str] = None) -> str:
    if username:
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user)
        except User.DoesNotExist:
            return Order.objects.none()
    return Order.objects.all()
