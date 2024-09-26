import datetime
from typing import Optional


from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime.datetime] = None
) -> None:
    user = User.objects.get(username=username)

    if date is not None:
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order.objects.create(user=user)
        order.created_at = date
        order.save()
    else:
        order = Order.objects.create(user=user)

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
