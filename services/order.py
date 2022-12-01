from db.models import Ticket, Order
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for info in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=info["movie_session"],
                row=info["row"],
                seat=info["seat"]
            )
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
