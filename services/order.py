from django.db import transaction

from db.models import Order
from db.models import User
from db.models import Ticket
from django.db.models import QuerySet


def create_order(tickets: dict, username: str, date: str = None) -> None:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=User.objects.get(username=username))
        if date:
            new_order.created_at = date
            new_order.save()
        for ticket in tickets:
            Ticket.objects.create(row=ticket["row"],
                                  seat=ticket["seat"],
                                  movie_session_id=ticket["movie_session"],
                                  order=new_order)


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
