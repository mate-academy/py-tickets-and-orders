from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.date = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        user.save()

        new_order = Order.objects.create(user=user)
        if date:
            new_order.created_at = date
        new_order.save()

        for ticket in tickets:
            new_ticket = Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            new_ticket.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
