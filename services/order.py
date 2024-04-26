from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            Ticket.objects.create(row=ticket["row"],
                                  seat=ticket["seat"],
                                  movie_session=ticket["movie_session"],
                                  order=order)
