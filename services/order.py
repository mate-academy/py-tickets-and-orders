import init_django_orm  # noqa: F401
from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


def create_order(tickets, username, date=None):
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username))
        if date:
            order.created_at = date
            order.save()
        for data in tickets:
            Ticket.objects.create(order=order,
                                  seat=data["seat"],
                                  row=data["row"],
                                  movie_session_id=data["movie_session"])
        return order


def get_orders(username=None):
    if username:
        return Order.objects.filter(
            user=get_user_model().objects.get(username=username))
    return Order.objects.all().order_by("-id")
