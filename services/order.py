from typing import List, Dict, Optional, Any

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: List[Dict[str, Any]],
        username: str,
        date: Optional[str] = None,
) -> Order:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        new_order = Order.objects.create(
            user=user
        )
        if date:
            new_order.created_at = date
            new_order.save()

        ordered_tickets = [
            Ticket(
                movie_session=MovieSession.objects.get(
                    pk=ticket.get("movie_session")
                ),
                order=new_order,
                row=ticket.get("row"),
                seat=ticket.get("seat")
            )
            for ticket in tickets
        ]
        Ticket.objects.bulk_create(ordered_tickets)

        return new_order


def get_orders(username: Optional[str] = None) -> List[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
