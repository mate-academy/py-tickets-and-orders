from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[int] = None
) -> Order:
    if username:
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )
    if date:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        row = ticket_data["row"]
        seat = ticket_data["seat"]
        movie_session_id = ticket_data["movie_session"]
        Ticket.objects.create(
            row=row,
            seat=seat,
            movie_session_id=movie_session_id,
            order=order
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.order_by("-user__username")
