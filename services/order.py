from datetime import datetime
from typing import List

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


def create_order(
    tickets: List[dict],
    username: str,
    date: datetime | None = None,
) -> None:
    user = get_user_model().objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date is not None:
            Order.objects.filter(id=order.id).update(created_at=date)
            order.created_at = date

        tickets_to_create = []

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket.get("movie_session")
            )

            tickets_to_create.append(
                Ticket(
                    row=ticket.get("row"),
                    seat=ticket.get("seat"),
                    movie_session=movie_session,
                    order=order,
                )
            )

        Ticket.objects.bulk_create(tickets_to_create)

def get_orders(
        username: str = None,
):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
