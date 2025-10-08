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
    if date:
        if isinstance(date, str):
            created_at = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        else:
            created_at = date
    else:
        created_at = datetime.datetime.now()

    order = Order(user=user, created_at=created_at)
    order.full_clean()
    order.save()

    for tt in tickets:
        movie_session = MovieSession.objects.get(id=tt["movie_session"])

        ticket = Ticket(
            order=order,
            movie_session=movie_session,
            row=tt["row"],
            seat=tt["seat"]
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
