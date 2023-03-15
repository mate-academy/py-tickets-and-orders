from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"],
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.order_by("-user")

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
