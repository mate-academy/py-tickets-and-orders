from typing import List

from django.db import transaction
from db.models import Order, Ticket, MovieSession
from db.models import User


@transaction.atomic
def create_order(tickets: List[Ticket], username: str, date=None) -> None:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        row = ticket_data["row"]
        seat = ticket_data["seat"]
        movie_session_id = ticket_data["movie_session"]

        movie_session = MovieSession.objects.get(id=movie_session_id)

        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat,
        )


def get_orders(username=None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
