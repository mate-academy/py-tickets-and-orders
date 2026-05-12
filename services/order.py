from django.db import transaction
from db.models import Order, Ticket
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from datetime import datetime
from typing import Optional, Any


@transaction.atomic
def create_order(
        tickets: list[dict[str, Any]],
        username: str,
        date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    if date:
        order = Order.objects.create(user=user)
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save(update_fields=["created_at"])
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"]
        )

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
