from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from django.db import transaction

User = get_user_model()


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> Order:
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        ticket_objects = []
        for ticket in tickets:
            row = ticket.get("row")
            seat = ticket.get("seat")
            movie_session_id = ticket.get("movie_session")

            if movie_session_id is None or row is None or seat is None:
                raise ValueError("Each ticket must have 'movie_session', "
                                 "'row', and 'seat' fields.")

            movie_session = MovieSession.objects.get(id=movie_session_id)

            ticket_objects.append(
                Ticket(
                    movie_session=movie_session,
                    order=order,
                    row=row,
                    seat=seat
                )
            )

        Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
