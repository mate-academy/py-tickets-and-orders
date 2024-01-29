from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:

    with transaction.atomic():

        order = Order.objects.create(user=User.objects.get(username=username),)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            tick = Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            tick.save()

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
