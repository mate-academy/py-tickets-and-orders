from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket, User, MovieSession
from django.db.models import QuerySet


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)
    order_ = Order.objects.create(user=user)

    if date:
        order_.created_at = date
        order_.save()

    for ticket in tickets:
        ticket = Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            ),
            order=order_
        )
        ticket.save()
    return order_


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)
    return orders
