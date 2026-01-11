import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket


@transaction.atomic
def create_order(tickets: list,
                 username: str,
                 date: str = None) -> None:
    user, _ = User.objects.get_or_create(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = (
            datetime.datetime.strptime(date, "%Y-%m-%d %H:%M"))
        order.save()

    for ticket in tickets:
        Ticket.objects.create(order=order,
                              row=ticket["row"],
                              seat=ticket["seat"],
                              movie_session_id=ticket["movie_session"])


def get_orders(username: str = None) -> QuerySet[Order, Order]:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))
    return Order.objects.all()
