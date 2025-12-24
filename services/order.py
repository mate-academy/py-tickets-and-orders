import datetime

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"]
            )
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
