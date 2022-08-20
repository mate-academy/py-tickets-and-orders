from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order


def create_order(tickets: list[dict], username: str, date: str = None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket_data["movie_session"],
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )

        return order


def get_orders(username: str = None):
    orders = Order.objects.all().order_by("-id")
    if username:
        return orders.filter(user__username=username)
    return orders
