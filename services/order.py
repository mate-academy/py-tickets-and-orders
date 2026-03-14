from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    if date:
        Order.objects.filter(pk=order.pk).update(created_at=date)

    movie_sessions = MovieSession.objects.all()
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session=movie_sessions.get(
                pk=ticket["movie_session"]
            ),
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
