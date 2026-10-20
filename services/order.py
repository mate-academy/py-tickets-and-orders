from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, User, Order


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        if date:
            date = datetime.fromisoformat(date)
        else:
            date = datetime.now()
        user = User.objects.get(username=username)
        order = Order.objects.create(
            created_at=date,
            user_id=user.id
        )
        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order_id=order.id
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
