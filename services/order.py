from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
import datetime

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: dict,
        username: str,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        _date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.created_at = _date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
