from datetime import datetime
from typing import List, Dict, Any, Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, MovieSession, Ticket

User = get_user_model()


def create_order(
    tickets: List[Dict[str, Any]],
    username: str,
    date: Optional[datetime] = None,
) -> Order:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User with username {username} does not exist.")
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date is not None:
            if isinstance(date, str):
                try:
                    date = datetime.strptime(date, "%Y-%m-%d %H:%M")
                except ValueError:
                    raise ValueError("Incorrect date format, "
                                     "should be YYYY-MM-DD HH:MM")
            order.created_at = date
            order.save()
        for ticket_data in tickets:
            row = ticket_data.get("row")
            seat = ticket_data.get("seat")
            movie_session_id = ticket_data.get("movie_session_id")
            if movie_session_id is None:
                movie_session_id = ticket_data.get("movie_session")

            if row is None or seat is None or movie_session_id is None:
                raise ValueError(
                    "Each ticket dictionary must contain row, "
                    "seat, and movie_session_id keys."
                )
            if not isinstance(movie_session_id, int):
                try:
                    movie_session_id = int(movie_session_id)
                except (ValueError, TypeError):
                    raise ValueError("movie_session_id (or movie_session) "
                                     "must be an integer.")

            try:
                movie_session = MovieSession.objects.get(id=movie_session_id)
            except ObjectDoesNotExist:
                raise ValueError(f"MovieSession with ID"
                                 f" {movie_session_id} does not exist.")

            try:
                Ticket.objects.create(
                    movie_session=movie_session,
                    order=order,
                    row=row,
                    seat=seat,
                )
            except ValidationError as e:
                raise e
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)
    return queryset
