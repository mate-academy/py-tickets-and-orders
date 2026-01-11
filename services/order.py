from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
    tickets: list,
    username: str,
    date: datetime = None,
) -> Order:
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )

        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
