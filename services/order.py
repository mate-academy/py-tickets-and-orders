from datetime import datetime
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth.password_validation import validate_password

from db.models import Order, Ticket, User, MovieSession


def validate_user_input(username: str, password: str) -> None:
    if not username or len(username) < 3:
        raise ValidationError("Username must be at least 3 characters long.")
    validate_password(password)


def create_order(
        tickets: list[dict[str, Any]],
        username: str,
        date: str = None
) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValidationError(
            f"User with username '{username}' does not exist."
        )

    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            try:
                created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
                order.created_at = created_at
            except ValueError:
                raise ValidationError(
                    "Date must be in the format 'YYYY-MM-DD HH:MM'."
                )
        order.save()

        for ticket in tickets:
            required_fields = {"row", "seat", "movie_session"}
            if not required_fields.issubset(ticket):
                raise ValidationError(
                    "Missing required ticket fields: "
                    "'row', 'seat', 'movie_session'."
                )

            try:
                movie_session = MovieSession.objects.get(
                    id=ticket["movie_session"]
                )
            except MovieSession.DoesNotExist:
                raise ValidationError(
                    f"Movie session with id '{ticket['movie_session']}'"
                    f" does not exist."
                )

            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie_session,
                order=order
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset.order_by("-id")
