from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)
    new_order = Order.objects.create(user=user)
    if date:
        new_order.created_at = date
        new_order.save()
    for ticket in tickets:
        ticket["movie_session_id"] = ticket["movie_session"]
        del ticket["movie_session"]
        Ticket.objects.create(**ticket, order=new_order)


def get_orders(username: str = None) -> QuerySet[Order]:
    user_orders = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        return user_orders.filter(user=user)
    return user_orders
