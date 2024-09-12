from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.query import QuerySet

from db.models import Order, Ticket


def create_order(tickets: list, username: str, date: str = None) -> None:
    with transaction.atomic():
        my_order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            my_order.created_at = date
            my_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=my_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
