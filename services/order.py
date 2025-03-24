from datetime import datetime
from typing import List, Dict, Any

from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, MovieSession, Ticket

from django.core.exceptions import ObjectDoesNotExist


def create_order(username, tickets, date=None):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with username {username} does not exist")

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            try:
                movie_session = MovieSession.objects.get(id=ticket["movie_session"])
            except MovieSession.DoesNotExist:
                raise ValueError(f"Movie session with id {ticket['movie_session']} does not exist")

            row = ticket["row"]
            seat = ticket["seat"]

            new_ticket = Ticket(
                row=row,
                seat=seat,
                movie_session=movie_session,
                order=order
            )
            new_ticket.save()

        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
