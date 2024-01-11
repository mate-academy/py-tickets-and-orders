from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
    tickets: list,
    username: str,
    date: str = None,
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
