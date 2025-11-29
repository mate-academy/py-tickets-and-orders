from typing import Optional, List, Dict
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket

# Pobieramy model użytkownika dynamicznie
User = get_user_model()


@transaction.atomic
def create_order(
        tickets: List[Dict[str, int]],
        username: str,
        date: Optional[str] = None,
) -> Order:
    """
    Create an order for a user with tickets.
    If date is provided, set created_at to this date.
    """
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    """
    Get all orders or filter by username.
    Returns a Django QuerySet.
    """
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs
