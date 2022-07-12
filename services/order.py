from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket


def create_order(tickets, username, date=None):
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )

        return order


def get_orders(username=None):
    orders = Order.objects.all().order_by("-id")
    if username:
        orders = orders.filter(user__username=username)
    return orders
