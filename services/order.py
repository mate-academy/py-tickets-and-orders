from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is None:
        return Order.objects.all()
    return Order.objects.filter(user__username=username)


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None
) -> None:
    order = Order.objects.create(
        user=User.objects.get(username=username)
    )
    if date is not None:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
