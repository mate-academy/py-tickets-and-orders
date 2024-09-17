from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list,
        username: str,
        date: datetime | None = None
) -> None:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_info in tickets:
            Ticket.objects.create(
                row=ticket_info["row"],
                seat=ticket_info["seat"],
                movie_session_id=ticket_info["movie_session"],
                order=order
            )


def get_orders(username: str | None = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders
