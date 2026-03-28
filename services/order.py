from typing import Optional
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from datetime import datetime

from db.models import Order, Ticket

users = get_user_model()


@transaction.atomic()
def create_order(
        tickets: list[Ticket],
        username: str,
        date: Optional[str] = None
) -> None:
    user_order = users.objects.get(username=username)
    new_order = Order.objects.create(user=user_order)

    if date:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        new_order.created_at = date
    new_order.save()

    users_tickets = []
    for ticket in tickets:
        new_ticket = Ticket(
            movie_session_id=ticket["movie_session"],
            order=new_order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
        new_ticket.clean()
        users_tickets.append(new_ticket)

    Ticket.objects.bulk_create(users_tickets)


def get_orders(username: Optional[str] = None) -> QuerySet:
    return (Order.objects.filter(user__username=username)
            if username
            else Order.objects.all())
