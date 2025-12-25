import datetime

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils import timezone
from django.shortcuts import get_object_or_404

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: str = None,
) -> Order:
    user = get_object_or_404(get_user_model(), username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        order.created_at = timezone.now()
    order.save()

    for ticket_data in tickets:
        movie_session_id = ticket_data["movie_session"]
        movie_session = get_object_or_404(MovieSession, id=movie_session_id)
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
