from django.contrib.auth import get_user_model
from django.db import transaction
from datetime import datetime
from db.models import Ticket, Order


def create_order(tickets: list, username: str, date: datetime = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()
        for item in tickets:
            Ticket.objects.create(
                row=item["row"],
                seat=item["seat"],
                movie_session_id=item["movie_session"],
                order_id=order.id,
            )


def get_orders(username: str = None) -> Order:
    if not username:
        return Order.objects.all()
    return Order.objects.filter(user__username=username)
