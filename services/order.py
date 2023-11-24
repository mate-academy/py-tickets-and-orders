from typing import Optional
from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket
from django.db.models.query import QuerySet


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        user_order = Order.objects.create(user=user)

        if date:
            user_order.created_at = date
            user_order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                order=user_order,
                movie_session_id=ticket_data.get("movie_session"),
                row=ticket_data.get("row"),
                seat=ticket_data.get("seat"),
            )

    return user_order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = Order.objects.filter(user__username=username)

    return orders
