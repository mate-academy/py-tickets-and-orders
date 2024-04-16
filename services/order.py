from datetime import datetime
from django.db.transaction import atomic
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket

User = get_user_model()


def create_order(tickets: list, username: str, date: datetime = None) -> None:
    with atomic():
        user_pk = User.objects.get(username=username).pk
        order = Order.objects.create(user_id=user_pk)
        if date:
            order.created_at = date
        order.save()
        for ticket in tickets:
            Ticket.objects.create(row=ticket["row"], seat=ticket["seat"],
                                  movie_session_id=ticket["movie_session"],
                                  order_id=order.pk)


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user_id=User.objects.get(username=username).pk)
    return orders
