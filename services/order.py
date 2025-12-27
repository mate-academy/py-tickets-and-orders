from typing import Any
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, MovieSession, Ticket


def get_orders(
        username: str = None
) -> QuerySet:
    queryset = Order.objects.all().order_by("-id")
    if username:
        queryset = queryset.filter(user__username=username).order_by("-id")

    return queryset


def create_order(
    tickets: list[dict[str, Any]],
    username: str,
    date: str = None
) -> Order:
    try:
        user = User.objects.get(username=username)  # Retrieve the user
    except User.DoesNotExist:
        raise ValidationError(f"User with username"
                              f" '{username}' does not exist.")

    with transaction.atomic():
        # Create the order
        order = Order.objects.create(user=user)
        if date:
            created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = created_at
        order.save()

        for ticket_data in tickets:
            required_fields = {"row", "seat", "movie_session"}
            if not required_fields.issubset(ticket_data):
                raise ValidationError("Missing required ticket fields")

            try:
                movie_session = MovieSession.objects.get(
                    id=ticket_data["movie_session"]
                )
            except MovieSession.DoesNotExist:
                raise ValidationError(f"Movie session with ID"
                                      f" {ticket_data['movie_session']}"
                                      f" does not exist.")

            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=movie_session,
                order=order
            )
    return order
