from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from services.movie_session import get_taken_seats


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> list[Ticket]:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)
    session_tickets = []

    if date:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        movie_session_id = ticket_data.get("movie_session")
        movie_session = MovieSession.objects.get(id=movie_session_id)
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")

        taken_seats = get_taken_seats(movie_session_id)

        if {"row": row, "seat": seat} in taken_seats:
            raise ValidationError(f"seat (row: {row}, seat: {seat}) "
                                  f"is already taken.")

        session_tickets.append(Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat
        ))
    return session_tickets


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is None:
        return Order.objects.all().values()

    user = get_user_model().objects.get(username=username)

    if not user:
        raise ValidationError(
            f"User with username '{username}' does not exist.")

    return Order.objects.filter(user=user).values()
