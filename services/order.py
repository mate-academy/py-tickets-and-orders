from typing import List, Dict, Optional
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
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(
                id=ticket_data["movie_session"]
            ),
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
