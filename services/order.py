import datetime
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: int, username: str, date: Optional[datetime] = None
) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError("User does not exist")

    order_kwargs = {"user": user}
    if date:
        parsed_date = parse_datetime(date)
        if not parsed_date:
            raise ValueError("Invalid date format")
        order_kwargs["created_at"] = parsed_date

    order = Order.objects.create(**order_kwargs)

    for ticket_data in tickets:
        try:
            movie_session = (
                MovieSession.objects.get(id=ticket_data["movie_session"])
            )
        except MovieSession.DoesNotExist:
            raise ValueError(
                f"Movie session {ticket_data['movie_session']} does not exist"
            )

        ticket = Ticket(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
        try:
            ticket.full_clean()
            ticket.save()
        except ValidationError as e:
            raise ValueError(f"Invalid ticket: {e.message_dict}")

    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
