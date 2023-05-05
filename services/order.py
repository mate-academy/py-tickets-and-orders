from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic()
def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[str] = None) -> Order:
    new_order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        new_order.created_at = date
    for ticket_data in tickets:
        Ticket.objects.create(
            order=new_order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    new_order.save()
    return new_order


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
