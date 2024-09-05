from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        ticket_objects = []
        for ticket in tickets:
            MovieSession.objects.get(pk=ticket["movie_session"])
            ticket_objects.append(Ticket(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
            ))

        Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
