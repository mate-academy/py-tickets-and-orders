from datetime import datetime

from db.models import Order, Ticket
from django.db import transaction
from db.models import User


def create_order(tickets: list[dict], username: str, date: datetime = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        new_order = Order.objects.create(user=user)

        ticket_instances = [
            Ticket(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=new_order,
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(ticket_instances)

        if date:
            new_order.created_at = date

        new_order.save()


def get_orders(username: str = None) -> None:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
