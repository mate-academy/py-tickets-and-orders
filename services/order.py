from django.db import transaction

from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model


def create_order(tickets: list, username: str, date: str = None):
    user_for_order = get_user_model().objects.get(username=username)
    new_order = Order(user=user_for_order)
    if date:
        new_order.created_at = date
    new_tickets = [
        Ticket(
            movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
            order=new_order,
            row=ticket["row"],
            seat=ticket["seat"]

        )
        for ticket in tickets
    ]
    with transaction.atomic():
        new_order.save()
        Ticket.objects.bulk_create(
            new_tickets
        )
