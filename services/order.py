from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    new_order = Order.objects.create(user=user)

    if date:
        new_order.created_at = date
        new_order.save(update_fields=["created_at"])

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=new_order,
            row=ticket["row"],
            seat=ticket["seat"]
        )

    return new_order


def get_orders(
        username: str | None = None
) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
