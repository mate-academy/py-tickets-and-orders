from typing import Iterable, Optional
from django.utils import timezone
from django.db import transaction
from db.models import Order, Ticket, User, MovieSession
from django.db.models import QuerySet


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username is None:
        return Order.objects.all()

    user = User.objects.filter(username=username).first()
    if not user:
        return Order.objects.none()

    return Order.objects.filter(user=user)


@transaction.atomic
def create_order(
    username: str,
    tickets: Iterable[dict],
    date: Optional[timezone.datetime] = None,
) -> Order:
    user = User.objects.get(username=username)

    if date is None:
        date = timezone.now()

    session_ids = []
    for ticket in tickets:
        session_id = (
            ticket.get("session_id")
            or ticket.get("session")
            or ticket.get("movie_session")
        )
        if session_id is None:
            raise KeyError("session_id")

        MovieSession.objects.get(id=session_id)
        session_ids.append(session_id)

    order = Order.objects.create(user=user)
    order.created_at = date
    order.save(update_fields=["created_at"])

    for ticket, session_id in zip(tickets, session_ids):
        movie_session = MovieSession.objects.get(id=session_id)

        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order
