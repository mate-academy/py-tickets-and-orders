from typing import Optional
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction
from django.utils import timezone
from db.models import Order, Ticket


def get_user(user_id: int):
    return get_user_model().objects.get(id=user_id)


def create_order(
    username: Optional[str] = None,
    user_id: Optional[int] = None,
    tickets: Optional[list[dict]] = None,
    date: Optional[datetime] = None,
) -> Order:
    if username:
        user = get_user_model().objects.get(username=username)
    elif user_id:
        user = get_user(user_id)
    else:
        raise ValueError("Either username or user_id must be provided")

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            created_at=date if date else timezone.now(),
        )

        if tickets:
            for ticket in tickets:
                s_id = (
                    ticket.get("movie_session_id")
                    or ticket.get("movie_session")
                )
                Ticket.objects.create(
                    order=order,
                    movie_session_id=s_id,
                    row=ticket["row"],
                    seat=ticket["seat"],
                )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs
