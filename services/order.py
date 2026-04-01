from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    if date is None:
        date = timezone.now()
    with transaction.atomic():

        user = User.objects.get(username=username)
        order = Order.objects.create(
            created_at=date,
            user=user)
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))
    return Order.objects.all()
