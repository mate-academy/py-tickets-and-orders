from typing import List

from django.db import transaction

from db.models import Ticket, Order, MovieSession
import datetime
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
        tickets: List[dict],
        username: str,
        date: datetime = None
) -> Order:

    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        if isinstance(date, str):
            new_created_at = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        else:
            new_created_at = date
        Order.objects.filter(id=order.id).update(created_at=new_created_at)
        order.refresh_from_db()

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )

        ticket = Ticket(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
        ticket.full_clean()
        ticket.save()

    return order


def get_orders(username: str = "") -> List[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(
            user=user
        ).prefetch_related(
            "tickets",
            "tickets__movie_session"
        )

    return Order.objects.all().prefetch_related(
        "tickets",
        "tickets__movie_session"
    )
