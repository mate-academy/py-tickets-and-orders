from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None,
) -> Order:
    user = get_object_or_404(User, username=username)

    order = Order.objects.create(
        user=user,
        created_at=datetime.strptime(date, "%Y-%m-%d %H:%M") if date else None,
    )

    for _ticket in tickets:
        movie_session = get_object_or_404(
            MovieSession, id=_ticket["movie_session"])

        ticket = Ticket(
            movie_session=movie_session,
            order=order,
            row=_ticket["row"],
            seat=_ticket["seat"],
        )
        ticket.full_clean()
        ticket.save()

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        user = get_object_or_404(User, username=username)
        return Order.objects.filter(user=user).order_by("-created_at")

    return Order.objects.all().order_by("-created_at")
