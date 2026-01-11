import datetime
from django.db import transaction, models
from django.contrib.auth import get_user_model

from db.models import Ticket, Order
from .movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(
    tickets: list[dict], username: str, date: datetime = None
) -> Order:
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

    return Order


@transaction.atomic
def get_orders(username: str = None) -> models.QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
