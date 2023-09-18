from datetime import datetime

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"]
            )

        return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
