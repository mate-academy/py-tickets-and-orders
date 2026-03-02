import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    try:
        user = get_user_model().objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist.")
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.datetime.strptime(
                date, "%Y-%m-%d %H:%M"
            )
            order.save()

        for ticket in tickets:
            Ticket(
                order=order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"]
            ).save()

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    query = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        query = query.filter(user=user)

    return query
