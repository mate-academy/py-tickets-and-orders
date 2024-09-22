from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        current_order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

        if date:
            current_order.created_at = date

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=current_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )

        current_order.save()


def get_orders(username: str = None) -> QuerySet:
    orders_queryset = Order.objects.all()

    if username:
        orders_queryset = orders_queryset.filter(user__username=username)

    return orders_queryset
