from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket
from django.contrib.auth import get_user_model

def create_order(
        tickets: list,
        username:str = None,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"]
            )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
