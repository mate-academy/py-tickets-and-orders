import datetime
from typing import List, Dict, Optional
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.db import transaction
from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save(update_fields=["created_at"])

    for ticket in tickets:
        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        row = ticket["row"]
        seat = ticket["seat"]

        if row < 1 or row > movie_session.cinema_hall.rows:
            raise ValidationError({
                "row": [
                    f"row number must be in available range: "
                    f"(1, rows): (1, {movie_session.cinema_hall.rows})"
                ]
            })
        if seat < 1 or seat > movie_session.cinema_hall.seats_in_row:
            raise ValidationError({
                "seat": [
                    f"seat number must be in available range: "
                    f"(1, seats_in_row): "
                    f"(1, {movie_session.cinema_hall.seats_in_row})"
                ]
            })

        if Ticket.objects.filter(
                movie_session=movie_session,
                row=row,
                seat=seat
        ).exists():
            raise ValidationError("Ticket already exists for this seat")

        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=row,
            seat=seat
        )

    return order


def get_orders(username: Optional[str] = None) -> "QuerySet[Order]":
    qs = Order.objects.all().order_by("-created_at")
    if username:
        qs = qs.filter(user__username=username)
    return qs
