from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(user=get_user_model().objects.get(username=username))
        if date:
            order.created_at = date
        order.save()
        for ticket_info in tickets:
            Ticket.objects.create(
                row=ticket_info["row"],
                seat=ticket_info["seat"],
                movie_session_id=ticket_info["movie_session"],
                order=order
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
