from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(tickets: list[dict], username: str, *,
                 date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(created_at=date, user=user)

        ticket_objects = [
            Ticket(
                seat=ticket["seat"],
                row=ticket["row"],
                movie_session_id=ticket["movie_session"],
                order=order
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(ticket_objects)
