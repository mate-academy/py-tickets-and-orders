from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:

    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    ticket_objects = []
    for ticket in tickets:
        ticket_objects.append(Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            order=order,
            movie_session=MovieSession.objects.get(
                pk=ticket["movie_session"]
            ),
        ))
    Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
