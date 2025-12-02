from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Ticket, Order


@transaction.atomic
def create_order(tickets: list[dict], username: str,
                 date: str = None) -> Order:

    selected_user = get_user_model().objects.get(username=username)

    user_order = Order.objects.create(user=selected_user)

    if date is not None:
        parsed_date = parse_datetime(date)
        Order.objects.filter(pk=user_order.pk).update(created_at=parsed_date)

    for ticket in tickets:
        Ticket.objects.create(order=user_order,
                              movie_session_id=ticket["movie_session"],
                              seat=ticket["seat"],
                              row=ticket["row"])

    return user_order


def get_orders(username: str = None) -> QuerySet[Order]:

    if username is not None:
        user = get_user_model().objects.get(username=username)

        return Order.objects.filter(user=user)

    return Order.objects.all()
