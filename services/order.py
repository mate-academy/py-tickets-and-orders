from typing import List, Dict, Any

from django.db import transaction
from django.contrib.auth import get_user_model

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: Ticket, username: User, date: str = None) -> str:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        ticket_order = [
            Ticket(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order
            )
            for ticket in tickets
        ]
        order.save()
        Ticket.objects.bulk_create(ticket_order)
        return order


def get_orders(username: User = None) -> List[Dict[str, Any]]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
