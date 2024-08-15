from datetime import datetime

from django.db import transaction
from django.utils import timezone

from db.models import Ticket, Order, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict], username: str, date: datetime = None
) -> Order:

    user = User.objects.get(username=username)
    order = Order.objects.create(
        user=user, created_at=date or timezone.now()
    )
    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            ),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
    return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
