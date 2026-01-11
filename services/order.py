from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    if date:
        new_order = Order.objects.create(
            user=get_user_model().objects.get(username=username),
            created_at=date,
        )
    else:
        new_order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            ),
            order_id=new_order.id,
            row=ticket["row"],
            seat=ticket["seat"],
        )


def get_orders(
        username: str = None
) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
