from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        try:
            order = Order.objects.create(
                user=User.objects.get(username=username),
            )
        except User.DoesNotExist as e:
            print(f"User {username} does not exist\n{e}")
        if date:
            if order:
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
    if username:
        return Order.objects.select_related(
            "user",
        ).filter(
            user__username=username
        )
    return Order.objects.all()
