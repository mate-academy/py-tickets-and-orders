from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"]
        )


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        user = User.objects.get(
            username=username
        )
        return Order.objects.filter(user_id=user.id)
    return Order.objects.all().order_by("-id")
