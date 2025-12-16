from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: str | None = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get_or_create(username=username)[0]
        )

        if date:
            order.created_at = date

        Ticket.objects.bulk_create(
            Ticket(
                movie_session=MovieSession.objects.get_or_create(
                    pk=ticket["movie_session"]
                )[0],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order,
            )
            for ticket in tickets
        )

        order.save()


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.prefetch_related()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
