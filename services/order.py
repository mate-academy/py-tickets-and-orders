from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list, username: str, date: datetime = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(order=order,
                              movie_session_id=ticket["movie_session"],
                              row=ticket["row"],
                              seat=ticket["seat"]
                              )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = Order.objects.filter(user__username=username)
    return queryset
