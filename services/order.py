from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str | None = None) -> None:
    user = get_user_model().objects.get(username=username)

    order = Order(user=user)
    order.save()

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(movie_session_id=ticket["movie_session"],
                              order=order,
                              row=ticket["row"],
                              seat=ticket["seat"])


def get_orders(username: str | None = None) -> QuerySet[Order]:
    orders_queryset = Order.objects.all()

    if username:
        orders_queryset = orders_queryset.filter(user__username=username)

    return orders_queryset
