from django.contrib.auth import get_user_model
from datetime import datetime
import init_django_orm  # noqa : F401

from django.db.models import QuerySet
from django.db import transaction
from db.models import Ticket, Order, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(
            user=user
        )

        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket in tickets:
            movie_session_id = ticket.get("movie_session")
            movie_session = MovieSession.objects.get(id=movie_session_id)
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket.get("row"),
                seat=ticket.get("seat")
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
