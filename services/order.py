from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            order.set_create_date(date)

        order.objects.bulk_create(tickets)


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
