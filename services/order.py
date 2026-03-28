from typing import List
from django.db import transaction
from db.models import Order, Ticket
from django.contrib.auth import get_user_model
from datetime import datetime


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:

    order = Order(user=get_user_model().objects.get(username=username))
    order.save()
    if date is not None:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    order.save()

    for ticket in tickets:
        ticket = Ticket(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
        )
        ticket.save()

    return order


def get_orders(username: str | None = None) -> List[Order]:
    orders = Order.objects.all()
    if username is not None:
        orders = orders.filter(user__username=username)
    return orders
