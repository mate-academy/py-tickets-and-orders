from django.db import transaction
from typing import Optional

from django.db.models import QuerySet

from db.models import MovieSession, User, Order, Ticket


def create_order(
        tickets: QuerySet,
        username: str,
        date: Optional[str] = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date is not None:
            order.created_at = date
        order.save()
        for ticket in tickets:
            movie_session = (
                MovieSession.objects.get(id=ticket["movie_session"])
            )

            row = ticket["row"]
            seat = ticket["seat"]
            Ticket.objects.create(
                order=order, movie_session=movie_session, row=row, seat=seat
            )


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)
    return queryset
