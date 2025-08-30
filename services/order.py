from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
        tickets: list,
        username:str = None,
        date: str = None
):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with username={username} not found")

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save(update_fields=["created_at"])
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                ticket=ticket,
                row=ticket["row"],
                seat=ticket["seat"]
            )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
