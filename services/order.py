from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from db.models import Order, Ticket
from django.db import transaction
from django.db.models import QuerySet


def str_to_date(date: str) -> datetime:
    year_month_day, hour_minutes = date.split()
    year_month_day = year_month_day.split("-")
    hour_minutes = hour_minutes.split(":")
    year_month_day = [int(item) for item in year_month_day]
    hour_minutes = [int(item) for item in hour_minutes]
    return datetime(*year_month_day, *hour_minutes)


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None) -> QuerySet[Order]:
    try:
        user = get_user_model().objects.get(username=username)
    except ObjectDoesNotExist:
        raise

    order = Order.objects.create(user=user)
    if date:
        date = str_to_date(date)
        print(date)
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket(movie_session_id=ticket["movie_session"],
               order=order,
               row=ticket["row"],
               seat=ticket["seat"]).save()

    return order


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
