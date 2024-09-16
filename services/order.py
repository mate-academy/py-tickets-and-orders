from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[datetime] = None) -> None:
    order = Order.objects.create(
        user=User.objects.get(username=username),
    )
    if date:
        order.created_at = date
        order.save()
    created_tickets = [
        Ticket(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        ) for ticket_data in tickets
    ]
    for ticket in created_tickets:
        ticket.full_clean()
    Ticket.objects.bulk_create(created_tickets)


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
