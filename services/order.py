from db.models import Order, Ticket
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.query import QuerySet
from typing import List


@transaction.atomic
def create_order(tickets: List[dict],
                 username: str,
                 date: str = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.date = date
    order.save()
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order
        )


def get_orders(username: str) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
