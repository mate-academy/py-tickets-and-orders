from datetime import datetime
from typing import List

from django.db import transaction

from db.models import Order, Ticket


def create_order(
        tickets: List[dict],
        username: str,
        date: datetime | None = None,
) -> None:
    with transaction.atomic():
        result_tickets = []
        list_of_orders = []
        for ticket in tickets:
            order = Order(
                username=username,
            )
            if date:
                order.date = date
            list_of_orders.append(order)
            new_ticket = Ticket(
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session=ticket.get("movie_session"),
                order=order
            )
            result_tickets.append(new_ticket)

        Ticket.objects.bulk_create(result_tickets)
        Order.objects.bulk_create(list_of_orders)


def get_orders(
        username: str = None,
):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
