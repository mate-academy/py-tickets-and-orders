from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = User.objects.filter(username=username)
    order = Order.objects.create(user=user, created_at=date)
    for ticket in tickets:
        Ticket.objects.create(order=order, **ticket)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
