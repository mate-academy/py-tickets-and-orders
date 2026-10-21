from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is None:
        return Order.objects.all()
    return Order.objects.filter(user__username=username)


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username),
    )
    if date is not None:
        Order.objects.filter(pk=order.pk).update(created_at=date)
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
