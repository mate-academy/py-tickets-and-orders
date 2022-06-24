from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(tickets: list[dict],
                 username,
                 date=None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)
        if date:
            new_order.created_at = date
            new_order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
