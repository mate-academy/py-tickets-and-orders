from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(tickets: list, username: str, date=None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"])


def get_orders(username=None):
    with transaction.atomic():
        orders = Order.objects.all()
        return orders.filter(user__username=username) if username else orders
