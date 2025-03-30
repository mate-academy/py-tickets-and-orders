from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> Order:

    user = get_user_model().objects.get(username=username)

    if not date:
        date = timezone.now()

    new_order = Order.objects.create(created_at=date, user=user)

    for ticket in tickets:
        movie_session_id = ticket.pop("movie_session")
        movie_session = MovieSession.objects.get(id=movie_session_id)
        Ticket.objects.create(
            order=new_order, movie_session=movie_session, **ticket
        )

    return new_order


def get_orders(username: str = None) -> QuerySet[Order]:

    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
