from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket, User


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None,
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(
            user=user
        )
        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            row = ticket["row"]
            seat = ticket["seat"]
            movie_session_id = ticket["movie_session"]

            Ticket.objects.create(
                order=order,
                row=row,
                seat=seat,
                movie_session_id=movie_session_id
            )


def get_orders(
        username: str | None = None
) -> list[dict]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
