from django.contrib.auth import get_user_model

import init_django_orm  # noqa: F401
from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order(
        user=get_user_model().objects.get(username=username),
        created_at=datetime.strptime(date, "%Y-%m-%d %H:%M")
        if date else datetime.now()
    )
    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(
                pk=ticket["movie_session"]
            ),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    result = Order.objects.all()
    if username:
        result = result.filter(user__username=username)
    return result
