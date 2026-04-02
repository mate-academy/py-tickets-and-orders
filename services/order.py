from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = Order(
            user=User.objects.get(username=username)
        )
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                seat=ticket["seat"],
                row=ticket["row"],
                order=order
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
