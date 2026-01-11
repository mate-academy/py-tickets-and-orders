from datetime import datetime
from typing import Optional

from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user = User.objects.get(username=username)

    if date is not None:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        created_at = datetime.now()

    order = Order.objects.create(
        user=user,
        created_at=created_at,
    )

    for ticket_data in tickets:
        movie_session = ticket_data["movie_session"]

        if isinstance(movie_session, int):
            movie_session = MovieSession.objects.get(id=movie_session)

        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
