from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list, username: str, date: datetime = None) -> None:
    with transaction.atomic():
        user, _ = User.objects.get_or_create(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            row = ticket.get("row")
            seat = ticket.get("seat")
            movie_session_id = ticket.get("movie_session")

            ticket = Ticket.objects.create(
                movie_session=MovieSession.objects.get(pk=movie_session_id),
                order=order,
                row=row,
                seat=seat
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
