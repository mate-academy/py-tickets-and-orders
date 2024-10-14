from datetime import datetime

from django.db.models import QuerySet

from db.models import Ticket, Order

from django.db import transaction


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime
) -> None:
    order = Order.objects.create(username=username)
    if date:
        order.created_at = date
    order.save()
    for ticket in tickets:
        ticket = Ticket.objects.create(
            movie_session=ticket.get("movie_session"),
            order=order,
            row=ticket.get("row"),
            seats=ticket.get("seat")
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(username=username)
    return Order.objects.all()
