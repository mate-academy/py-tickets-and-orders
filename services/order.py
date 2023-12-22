from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:

    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = date_obj
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order_id=order.id,
                row=ticket["row"],
                seat=ticket["seat"]
            )
        return order


def get_orders(username: Optional[str] = None) -> Order:
    queryset = Order.objects.all()

    if username:
        queryset = Order.objects.filter(user__username=username)

    return queryset
