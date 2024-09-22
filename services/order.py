from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> None:
    get_user = get_user_model().objects.get(
        username=username)
    new_order, _ = Order.objects.get_or_create(
        user=get_user
    )
    if date:
        parsed_date = parse_datetime(date)
        new_order.created_at = parsed_date
        new_order.date = parsed_date
        new_order.save()

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            order=new_order,
            movie_session=MovieSession.objects.get(pk=ticket["movie_session"])
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
