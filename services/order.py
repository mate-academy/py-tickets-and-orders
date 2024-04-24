from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

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
    order = Order.objects.all()
    if username:
        order = Order.objects.filter(user__username=username)
    return order
