import init_django_orm  # noqa: F401
import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: dict,
        username: str,
        date: Optional[datetime.datetime] = None
) -> Order:
    order = Order.objects.create(user=User.objects.get(username=username))
    for ticket in tickets:
        Ticket.objects.create(
            seat=ticket["seat"],
            row=ticket["row"],
            movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
            order=order,
        )
    if date is not None:
        order.created_at = date
    return order.save()


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders = Order.objects.all()
    if username is not None:
        orders = orders.filter(user__username=username)
    return orders
