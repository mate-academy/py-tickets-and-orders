import init_django_orm  # noqa: F401

from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket


def create_order(tickets: list[dict], username, date=None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for data in tickets:
            Ticket.objects.create(
                order=order,
                row=data["row"],
                seat=data["seat"],
                movie_session_id=data["movie_session"],
            )

    return order


def get_orders(username=None):
    if username:
        return Order.objects.filter(
            user=get_user_model().objects.get(username=username)
        )

    return Order.objects.all()
