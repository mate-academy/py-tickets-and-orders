from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:

    user = get_user_model().objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        for ticket in tickets:
            movie_session_id = ticket.get("movie_session")
            row = ticket.get("row")
            seat = ticket.get("seat")

            movie_session = MovieSession.objects.get(pk=movie_session_id)

            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=row,
                seat=seat
            )

        order.save()
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
