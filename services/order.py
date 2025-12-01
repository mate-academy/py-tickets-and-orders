from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession
from django.contrib.auth import get_user_model

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None
) -> Order:
    user = User.objects.get(username=username)
    if date:
        order = Order.objects.create(user=user, created_at=date)
    else:
        order = Order.objects.create(user=user)

    for ticket in tickets:
        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = (
        Order.objects.
        select_related("user")
        .prefetch_related("tickets")
    )
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
