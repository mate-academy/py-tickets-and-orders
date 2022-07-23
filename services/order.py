from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(tickets: list[dict], username: str, date=None):

    with transaction.atomic():
        user = get_user_model().objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"])


def get_orders(username=None):
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)

    return Order.objects.all()
