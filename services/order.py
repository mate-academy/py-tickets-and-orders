from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )
        if date:
            order.created_at.set(date)

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session=ticket.get("movie_session")
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
