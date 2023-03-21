from datetime import datetime
from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


def create_order(tickets: list, username: str, date: datetime = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)
        if date:
            new_order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order_id=new_order.id,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
