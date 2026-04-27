from typing import List, Dict, Optional

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: List[Dict],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    ticket_objects = []

    for ticket in tickets:
        ticket_objects.append(
            Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )
        )

    for ticket in ticket_objects:
        ticket.save()

    return order


def get_orders(username: Optional[str] = None) -> Order:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
