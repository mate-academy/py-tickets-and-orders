from typing import List, Dict, Optional
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


User = get_user_model()


@transaction.atomic
def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None
) -> List[Ticket]:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist.")

    order = Order.objects.create(user=user)

    if date:
        try:
            custom_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Date must be in format 'YYYY-MM-DD HH:MM'")

        order.created_at = custom_date
        order.save(update_fields=["created_at"])

    created_tickets = []

    for data in tickets:
        movie_session = MovieSession.objects.get(id=data["movie_session"])
        ticket = Ticket(
            movie_session=movie_session,
            order=order,
            row=data["row"],
            seat=data["seat"]
        )
        ticket.full_clean()
        ticket.save()
        created_tickets.append(ticket)

    return created_tickets


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
