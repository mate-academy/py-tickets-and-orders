from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.db.models import QuerySet

from db.models import Ticket, Order

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None
) -> None:
    user = User.objects.get(username=username)
    created_at = parse_datetime(date) if date else None

    if created_at:
        order = Order.objects.create(user=user, created_at=created_at)
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        movie_session_id = ticket_data["movie_session"]
        row = ticket_data["row"]
        seat = ticket_data["seat"]

        if Ticket.objects.filter(
            movie_session_id=movie_session_id,
            row=row,
            seat=seat
        ).exists():
            raise ValueError(f"Місце {row}-{seat} вже зайняте")

        Ticket.objects.create(
            order=order,
            movie_session_id=movie_session_id,
            row=row,
            seat=seat
        )


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username is None:
        return Order.objects.all()
    if username == "":
        return Order.objects.none()
    return Order.objects.filter(user__username=username)
