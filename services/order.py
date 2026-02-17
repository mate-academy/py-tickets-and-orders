from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, User, Order
from datetime import datetime


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None) -> Order:

    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=date)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"])
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all().order_by("-created_at")
