import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = get_user_model().objects.get(username=username)

    if date:
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            order = Order.objects.create(user=user, created_at=date)
        else:
            order = Order.objects.create(user=user, created_at=date)
    else:
        order = Order.objects.create(user=user)
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"])
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    query = Order.objects.all()
    if username:
        query = query.filter(user__username=username)
    return query
