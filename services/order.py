from typing import List, Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


def create_order(
        tickets: List[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user_name = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user_name)

        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
        return new_order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        return orders.filter(user__username=username)
    return orders
