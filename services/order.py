from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
        tickets: list,
        username: str,
        date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            parsed_date = datetime.fromisoformat(date)
            order.created_at = parsed_date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order,
            )


def get_orders(username: str = None) -> QuerySet | None:
    try:
        if username:
            return Order.objects.filter(
                user=User.objects.get(username=username)
            )
        else:
            return Order.objects.all()
    except User.DoesNotExist:
        return None
