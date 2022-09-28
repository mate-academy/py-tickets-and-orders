from django.db import transaction
from db.models import Order, Ticket, User
from datetime import datetime


def create_order(tickets: list, username: str, date: datetime = None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order,
            )


def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all().order_by("-id")
