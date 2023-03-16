from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction

from db.models import Ticket, Order


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    created_tickets = []
    for ticket in tickets:
        created_tickets.append(
            Ticket.objects.create(
                seat=ticket["seat"],
                row=ticket["row"],
                movie_session_id=ticket["movie_session"],
                order=order
            ))


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        return queryset.filter(user__username=username)
    return queryset
