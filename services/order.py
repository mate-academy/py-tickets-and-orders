import datetime
from django.db import transaction
from django.db.models import QuerySet

from db.models import (
    Ticket,
    Order,
    User,
    MovieSession
)


def create_order(
    tickets: list[dict],
    username: str,
    date: datetime.datetime = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(
            user=user
        )

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    pk=ticket_data["movie_session"]
                ),
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )


def get_orders(
        username: str = None
) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        user = User.objects.get(username=username)

        queryset = queryset.filter(user_id=user.id)

    return queryset
