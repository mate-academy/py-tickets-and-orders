from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date is not None:
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket["movie_session"]
            )
            tik = Ticket(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"])
            tik.full_clean()
            tik.save()


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username is None:
        return Order.objects.all()
    return Order.objects.filter(user__username=username)
