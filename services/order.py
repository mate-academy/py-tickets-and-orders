from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession, User


def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(
            user=user,
        )
        if date:
            order.created_at = date
        order.save()

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )
            row = ticket_data["row"]
            seat = ticket_data["seat"]

            ticket = Ticket(
                row=row,
                seat=seat,
                movie_session=movie_session,
                order=order
            )
            ticket.save()

        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
