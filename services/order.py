from datetime import datetime
from django.db.models import QuerySet
from django.db import transaction

from db.models import Order, Ticket, MovieSession, User


def create_order(
        tickets: list[dict],
        username: str, date:
        datetime = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        ticket_instances = []
        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket_data["movie_session"]
            )
            ticket_instances.append(Ticket(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=movie_session,
                order=order
            ))

        Ticket.objects.bulk_create(ticket_instances)


def get_orders(username: str = None) -> Order | QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
