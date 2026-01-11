from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    user_1 = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user_1)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    for ticket in tickets:
        Ticket.objects.create(movie_session_id=ticket.get("movie_session"),
                              order=order,
                              row=ticket.get("row"),
                              seat=ticket.get("seat"))
    order.save()
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(
            user=get_user_model().objects.get(
                username=username))
    return orders
