from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import MovieSession, Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str = None,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            ),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
