from datetime import datetime
from typing import List, Dict, Optional

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


def create_order(
    tickets: List[Dict],
    username: str,
    date: Optional[str] = None,
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            created_at = datetime.fromisoformat(date)
            order.created_at = created_at
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
    queryset = Order.objects.select_related("user").all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
