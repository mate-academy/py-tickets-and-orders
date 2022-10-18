from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import DateTimeField, QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[Ticket],
        username: str,
        date: DateTimeField = None
) -> None:

    with transaction.atomic():
        customer = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=customer)

        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session_id=ticket.get("movie_session"),
                order=new_order
            )


def get_orders(
        username: str = None
) -> QuerySet:
    queryset = Order.objects.all().order_by("-user")

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
