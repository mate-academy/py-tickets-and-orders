from db.models import Order
from db.models import Ticket
from db.models import MovieSession
from datetime import datetime
from db.models import User
from typing import List, Dict, Union, Optional

from django.db.models import QuerySet
from django.db import transaction


def create_order(tickets: List[Dict[str, Union[int, str]]],
                 username: str,
                 date: Optional[Union[str, datetime]] = None) -> Order:
    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError("User not found")

        if not date:
            date = datetime.utcnow()

        order = Order.objects.create(user_id=user.id)

        order.created_at = date
        order.save()

        for ticket_data in tickets:
            try:
                movie_session = MovieSession.objects.get(
                    pk=ticket_data["movie_session"])
            except MovieSession.DoesNotExist:
                raise ValueError(f"Movie session "
                                 f"{ticket_data['movie_session']} not found")

            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=movie_session,
                order=order
            )

        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()

    return orders
