from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order, Ticket


def create_order(tickets: list,
                 username: str,
                 date: datetime = None,
                 ) -> None:
    with transaction.atomic():
        user_model = get_user_model()
        user = user_model.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order_id=order.id,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    order = Order.objects.all()
    if username:
        order = Order.objects.filter(user__username=username)
    return order
