from django.db import transaction
from django.db.models import QuerySet

from datetime import datetime

from db.models import Order, Ticket, User


def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )


def get_orders(username: str = None) -> QuerySet(Order):
    query = Order.objects.all()
    if username:
        query = query.filter(user__username=username)
    return query
