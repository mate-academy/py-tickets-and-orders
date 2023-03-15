from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(tickets: list, username: str, date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user_id=user.id)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.order_by("-user")
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
