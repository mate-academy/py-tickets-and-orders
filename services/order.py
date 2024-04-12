from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None,
) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        new_ticket = Ticket.objects.create(
            order=order,
            movie_session=MovieSession.objects.get(
                pk=ticket["movie_session"]
            ),
            row=ticket["row"],
            seat=ticket["seat"])
        new_ticket.save()

    return order


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
