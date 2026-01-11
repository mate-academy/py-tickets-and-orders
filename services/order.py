from typing import Optional
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import QuerySet


from db.models import Order, User, MovieSession, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None,
) -> Order:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User {username} does not exist")

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date is not None:
            if isinstance(date, str):
                try:
                    date = date = datetime.strptime(date, "%Y-%m-%d %H:%M")
                except ValueError:
                    raise ValueError("Date must be "
                                     "formatted as %Y-%m-%d %H:%M")
            order.created_at = date
            order.save()

        for ticket in tickets:
            row = ticket.get("row")
            seat = ticket.get("seat")
            movie_session_id = ticket["movie_session"]
            if row is None or seat is None or movie_session_id is None:
                raise ValueError(
                    "Each ticket dictionary must contain row, "
                    "seat, and movie_session keys."
                )
            try:
                movie_session = MovieSession.objects.get(id=movie_session_id)
            except ObjectDoesNotExist:
                raise ValueError(f"Movie session id "
                                 f"{movie_session_id} does not exist")
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


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)
    return queryset
