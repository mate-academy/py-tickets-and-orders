from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket
from services.movie_session import get_movie_session_by_id


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:

    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = get_movie_session_by_id(ticket["movie_session"])
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
