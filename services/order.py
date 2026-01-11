from typing import List, Dict, Any

from django.db.models import QuerySet

from db.models import Order, Ticket, User
from django.db import transaction


@transaction.atomic
def create_order(
        tickets: List[Dict[str, Any]],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user, created_at=date)

    if not user:
        raise Exception("User doesn't exist")

    if date:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
