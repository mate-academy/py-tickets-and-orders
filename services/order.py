from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Ticket, Order
from django.db import transaction

from services.movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(
        user=user,
    )
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=get_movie_session_by_id(ticket["movie_session"]),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )


def get_orders(
        username: str = None,
) -> QuerySet:
    if username:
        return Order.objects.filter(
            user=get_user_model().objects.get(username=username)
        )
    return Order.objects.all()
