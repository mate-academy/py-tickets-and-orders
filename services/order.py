from datetime import datetime

from django.db import transaction

from db.models import Order
from db.models import Ticket
from db.models import User
from db.models import MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:
    user = User.objects.get(username=username)
    if date:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order.objects.create(created_at=date, user=user)
    else:
        order = Order.objects.create(user=user)
    ticket_obj = [
        Ticket(
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            ),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
        for ticket in tickets
    ]
    Ticket.objects.bulk_create(ticket_obj)


def get_orders(username: str | None = None) -> list[dict]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
