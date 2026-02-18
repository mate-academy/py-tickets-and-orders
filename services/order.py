from django.contrib.auth import get_user_model
from datetime import datetime

from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from django.db import transaction


@transaction.atomic
def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save(update_fields=["created_at"])

    for ticket in tickets:

        if not all(k in ticket for k in ("row", "seat", "movie_session")):
            raise ValueError(
                "Each ticket must have 'row', 'seat', and 'movie_session'."
            )

        session = MovieSession.objects.get(pk=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )

    return order


def get_orders(username: str = None) -> QuerySet:

    if username:
        user = get_user_model().objects.get(username=username)
        return user.orders.all()

    return Order.objects.all()
