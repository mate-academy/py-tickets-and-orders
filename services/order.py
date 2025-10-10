from django.db import transaction
from datetime import datetime
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket
from typing import Optional, Union


@transaction.atomic
def create_order(tickets: list, username: str,
                 date: Optional[Union[str, datetime]] = None) -> Order:
    user = get_user_model()
    user = user.objects.get(username=username)
    parsed_date = None
    if isinstance(date, str):
        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    elif isinstance(date, datetime):
        parsed_date = date

    if parsed_date:
        order = Order.objects.create(user=user, created_at=parsed_date)
    else:
        order = Order.objects.create(user=user)

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
            )

        return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.objects.get(username=username)

    return queryset
