from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    order = Order.objects.create(user__username=username)
    if date:
        order.created_at = date

    tickets_list = [
        Ticket(**ticket_info, order=order)
        for ticket_info in tickets
    ]

    Ticket.objects.bulk_create(tickets_list)


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders
