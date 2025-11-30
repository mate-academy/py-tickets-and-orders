from typing import List

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(tickets: List[dict],
                 username: str,
                 date: str = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(
        user=user
    )
    if date:
        order.created_at = date
    order.save()

    ticket_objects = []
    for ticket in tickets:
        try:
            ms = MovieSession.objects.get(id=ticket["movie_session"])
        except MovieSession.DoesNotExist:
            raise ValidationError(
                f"MovieSession {ticket['movie_session']} does not exist")
        ticket_objects.append(
            Ticket(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=ms,
                order=order
            )
        )

    Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
