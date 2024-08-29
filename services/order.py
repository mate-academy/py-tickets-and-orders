from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            created_at=date if date else None
        )
        for ticket_data in tickets:
            Ticket.objects.create(order=order, **ticket_data)
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
