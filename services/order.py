from typing import Optional, List, Dict
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(
        user=user, created_at=date if date else timezone.now()
    )

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
