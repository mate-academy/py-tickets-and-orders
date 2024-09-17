from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None,
) -> None:

    user_add = User.objects.get(username=username)
    new_order = Order.objects.create(user=user_add)
    if date:
        new_order.created_at = date
        new_order.save()
    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=(MovieSession.objects.get
                           (id=ticket["movie_session"])),
            order=new_order,
        )


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        queryset = queryset.filter(user=user)
    return queryset
