import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from typing import TypedDict, List


class TicketType(TypedDict):
    row: int
    seat: int
    movie_session: int


type TicketsList = List[TicketType]


@transaction.atomic
def create_order(
    tickets: TicketType,
    username: str,
    date: str | datetime.date | None = None,
) -> None:
    user = get_user_model().objects.get(username=username)

    new_order = Order.objects.create(user=user)

    if date:
        if isinstance(date, str):
            date = datetime.datetime.fromisoformat(date)
        Order.objects.filter(id=new_order.id).update(created_at=date)

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=new_order,
        )


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
