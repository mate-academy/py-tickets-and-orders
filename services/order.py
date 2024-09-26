from django.contrib.auth import get_user_model
from django.db import transaction
from typing import Optional
from db.models import Order, Ticket
from django.db.models import QuerySet


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None
) -> QuerySet:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()
        for ticket_data in tickets:
            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"],
                order=order
            )

        return order


def get_orders(
        username: Optional[str] = None,
) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
