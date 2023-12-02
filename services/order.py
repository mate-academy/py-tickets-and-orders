from django.db import transaction

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user, created_at=date)
    for ticket in tickets:
        Ticket.objects.create(order=order, **ticket)


def get_orders(username: str = None) -> models.QuerySet[Order]:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
