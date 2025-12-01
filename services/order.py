from django.db import transaction
from django.db.models import QuerySet
import datetime

from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None,
):
    User = get_user_model()
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        created_at = parse_datetime(date)
        if created_at:
            Order.objects.filter(pk=order.pk).update(created_at=created_at)
            order.refresh_from_db()
    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(id=ticket_data["movie_session"])
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    return order

def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()