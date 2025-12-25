from datetime import datetime
from typing import Optional

from django.db.transaction import atomic
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket

User_model = get_user_model()


def create_order(tickets: list,
                 username: str,
                 date: Optional[datetime] = None) -> None:
    with atomic():
        user_pk = User_model.objects.get(username=username).pk
        order = Order.objects.create(user_id=user_pk)
        if date:
            order.created_at = date
        order.save()
        for ticket in tickets:
            Ticket.objects.create(row=ticket["row"], seat=ticket["seat"],
                                  movie_session_id=ticket["movie_session"],
                                  order_id=order.pk)


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
