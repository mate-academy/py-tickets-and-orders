from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order_id=order.id,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
