from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    if date:
        order = Order.objects.create(
            user=user,
            created_at=date
        )
    else:
        order = Order.objects.create(
            user=user
        )

    raw_tickets = [
        Ticket(
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            ),
            row=ticket["row"],
            seat=ticket["seat"],
            order=order
        )
        for ticket in tickets
    ]

    Ticket.objects.bulk_create(raw_tickets)


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
