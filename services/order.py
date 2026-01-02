from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict], username: str, date: datetime | None = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        Ticket.objects.bulk_create(
            [Ticket(
                order=order,
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                row=ticket["row"],
                seat=ticket["seat"]
            ) for ticket in tickets]
        )
        return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
