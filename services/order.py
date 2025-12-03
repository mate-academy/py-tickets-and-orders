from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None
) -> Order:
    from django.utils import timezone
    user = get_user_model().objects.get(username=username)
    created_at = date or timezone.now()
    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=created_at)
        for tick in tickets:
            movie_session = MovieSession.objects.get(id=tick["movie_session"])
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=tick["row"],
                seat=tick["seat"]
            )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
