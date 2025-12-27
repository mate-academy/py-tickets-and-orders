from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None,
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            order.created_at = date
        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                movie_session=MovieSession.objects.get(
                    id=ticket_data["movie_session"]
                ),
                row=ticket_data["row"],
                seat=ticket_data["seat"],
            )
        order.save()

        return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
