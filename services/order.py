from typing import Optional
from django.db.models import QuerySet
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.dateparse import parse_datetime
from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    if date:
        created_at = parse_datetime(date)
    else:
        created_at = timezone.now()

    order = Order.objects.create(user=user, created_at=created_at)

    for ticket_data in tickets:
        movie_session = (
            MovieSession.objects.get(id=ticket_data["movie_session"]))
        ticket = Ticket(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
        ticket.full_clean()
        ticket.save()

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.select_related("user")
    if username:
        orders = orders.filter(user__username=username)
    return orders
