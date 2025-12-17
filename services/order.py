from typing import Optional
from django.db import transaction
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: Optional[str] = None
) -> Order:
    """
    Create order with tickets.
    """
    user_model = get_user_model()
    user = user_model.objects.get(username=username)

    order = Order(user=user)
    order.save()

    if date is not None:
        if isinstance(date, str):
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        else:
            order.created_at = date
        order.save(update_fields=["created_at"])  # ← Подвійні лапки

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:

    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
