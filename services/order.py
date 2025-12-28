from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


User = get_user_model()


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"]
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user).order_by("id")
    return Order.objects.all().order_by("-created_at", "id")
