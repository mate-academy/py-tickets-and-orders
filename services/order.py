from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from typing import List, Dict, Optional, Union
from datetime import datetime

from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: List[Dict[str, Union[int, str]]],
        username: str,
        date: Optional[datetime] = None
) -> Order:
    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValueError(
                f"User with username '{username}' not found."
            )

        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for tickets_data in tickets:
            try:
                movie_session = MovieSession.objects.get(
                    id=tickets_data["movie_session"]
                )
            except ObjectDoesNotExist:
                raise ValueError(
                    f"MovieSession with ID "
                    f"{tickets_data['movie_session']} not found."
                )

            tickets_data["movie_session"] = movie_session
            Ticket.objects.create(order=order, **tickets_data)

        return order


def get_orders(
        username: Optional[str] = None,
) -> QuerySet:
    if username:
        try:
            return Order.objects.filter(user__username=username)
        except ObjectDoesNotExist:
            raise ValueError(f"Orders for user '{username}' not found.")
    return Order.objects.all()
