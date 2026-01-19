from datetime import datetime
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.utils.timezone import now

from db.models import Ticket, User, Order, MovieSession


def create_order(tickets: list[dict[str, Any]],
                 username: str, date: datetime = None) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist.")

    try:
        with transaction.atomic():
            order = Order.objects.create(
                user=user, created_at=date if date else now()
            )

            for ticket_data in tickets:
                try:
                    movie_session = MovieSession.objects.get(
                        id=ticket_data["movie_session"]
                    )
                except MovieSession.DoesNotExist:
                    raise ValueError(
                        f"MovieSession with id"
                        f" {ticket_data["movie_session"]} does not exist."
                    )

                try:
                    Ticket.objects.create(
                        movie_session=movie_session,
                        order=order,
                        row=ticket_data["row"],
                        seat=ticket_data["seat"],
                    )
                except IntegrityError:
                    raise ValueError(
                        f"Ticket for row {ticket_data["row"]} "
                        f"and seat {ticket_data["seat"]} "
                        f"already exists in the movie session."
                    )
            return order
    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")


def get_orders(username: str = None) -> Any:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
