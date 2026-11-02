from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Ticket, Order
from django.db import transaction

from datetime import datetime


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    name = get_user_model().objects.get(username=username)
    new_order = Order.objects.create(user=name)
    if date:
        new_order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        new_order.save()

    for ticket in tickets:
        Ticket.objects.create(movie_session_id=ticket["movie_session"],
                              seat=ticket["seat"],
                              row=ticket["row"],
                              order=new_order)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
