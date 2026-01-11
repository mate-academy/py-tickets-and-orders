from datetime import datetime

from django.db.models import QuerySet
import init_django_orm  # noqa : F401
from db.models import Order, Ticket, MovieSession
from django.db import transaction
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(
        user=user
    )

    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()
    for ticket in tickets:
        movie_session_id = ticket.get("movie_session")
        movie_session = MovieSession.objects.get(id=movie_session_id)
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
