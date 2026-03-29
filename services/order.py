from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import DateTimeField, QuerySet

from db.models import Order, Ticket


def create_order(tickets: list[Ticket], username: str,
                 date: DateTimeField = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for each_ticket in tickets:
            Ticket.objects.create(
                movie_session_id=each_ticket["movie_session"],
                order=order,
                row=each_ticket["row"],
                seat=each_ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all().order_by("-user")
    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
