from typing import Optional

from services.user import User
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[str] = None
                 ) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        movies_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=movies_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        return Order.objects.filter(user__username=username)
    return queryset
