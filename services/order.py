from typing import List

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from datetime import datetime

from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: List[dict],
                 username: str,
                 date: datetime = None) -> Order:
    try:
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user,)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(order=order,
                                  row=ticket.get("row"),
                                  seat=ticket.get("seat"),
                                  movie_session_id=ticket.get("movie_session")
                                  )
        return order
    except get_user_model().DoesNotExist:
        raise ValidationError(f"{username} is not a valid user")


def get_orders(username: str = None) -> QuerySet:
    if username:
        try:
            user = get_user_model().objects.get(username=username)
            return user.orders.all()
        except get_user_model().DoesNotExist:
            raise ValidationError(f"{username} is not a valid user")
    return Order.objects.all()
