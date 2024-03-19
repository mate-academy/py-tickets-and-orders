from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket


def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None,
) -> Order:
    with transaction.atomic():
        if tickets and username:
            order = Order.objects.create()
            if date:
                order.created_at = date
            order.user.username = username
            order.save()

            return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
