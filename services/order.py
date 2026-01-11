from datetime import datetime
from typing import List

from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order, User, MovieSession


@transaction.atomic
def create_order(tickets: List[dict], username: str, date: str = None) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket["movie_session"]
        )
        Ticket.objects.create(order=order,
                              movie_session=movie_session,
                              row=ticket["row"],
                              seat=ticket["seat"])


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders
