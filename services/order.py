from datetime import datetime
from django.db import transaction
from django.db.models.query import QuerySet
from db.models import Order, Ticket
from services.user import get_user_by_username
from typing import List, Optional


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all().order_by("-created_at")
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset


@transaction.atomic
def create_order(
    tickets: List[dict],
    username: str,
    date: Optional[str] = None
) -> Order:
    user = get_user_by_username(username)

    order = Order.objects.create(user=user)

    if date:
        created_at = datetime.fromisoformat(date)
        Order.objects.filter(id=order.id).update(created_at=created_at)

    for ticket_data in tickets:
        ticket = Ticket(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
        ticket.full_clean()
        ticket.save()

    return order
