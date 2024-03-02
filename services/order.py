from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> Order:
    with transaction.atomic():
        order_user = User.objects.get(username=username)
        order = Order.objects.create(user=order_user)

        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            row = ticket["row"]
            seat = ticket["seat"]
            movie_session_id = ticket["movie_session"]

            Ticket.objects.create(
                order=order,
                movie_session_id=movie_session_id,
                row=row,
                seat=seat
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
