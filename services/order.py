from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        if not user:
            raise ValidationError("No user with this name")
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        [
            order.tickets.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
            )
            for ticket in tickets
        ]


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.all().filter(user__username=username)
    return Order.objects.all()
