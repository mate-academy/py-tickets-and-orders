from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id


user = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | datetime | None = None,
) -> Order:
    db_user = user.objects.get(username=username)
    created_at = date if date is not None else timezone.now()
    order = Order.objects.create(user=db_user, created_at=created_at)
    for ticket in tickets:
        Ticket.objects.create(
            movie_session=get_movie_session_by_id(ticket.get("movie_session")),
            order=order,
            row=ticket.get("row"),
            seat=ticket.get("seat"),
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if not username:
        return Order.objects.all()

    return Order.objects.select_related("user").filter(user__username=username)
