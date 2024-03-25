from typing import List, Dict

from django.db.models import QuerySet
from django.db import transaction

from db.models import Order, Ticket, User


def create_order(tickets: List[Dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            row, seat, session_id = ticket.values()
            Ticket.objects.create(
                movie_session_id=session_id,
                order=order,
                row=row,
                seat=seat
            )
        return


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))
    return Order.objects.all()
