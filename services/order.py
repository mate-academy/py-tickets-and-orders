from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(tickets: list[dict], username: str,
                 date: datetime = None) -> Order:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order(user=user)
        order.save()

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            new_ticket = Ticket(movie_session_id=ticket["movie_session"],
                                order=order,
                                row=ticket["row"],
                                seat=ticket["seat"])
            new_ticket.save()
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
