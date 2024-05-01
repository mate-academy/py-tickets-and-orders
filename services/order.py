import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)

        if date:
            new_order.created_at = date
            new_order.save()

        for ticket_data in tickets:
            movie_session_id = ticket_data.pop("movie_session")
            movie_session = MovieSession.objects.get(pk=movie_session_id)
            new_ticket = Ticket(
                order=new_order,
                movie_session=movie_session,
                **ticket_data
            )
            new_ticket.save()


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
