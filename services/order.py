from datetime import datetime

from django.db import transaction
from db.models import Order, Ticket, User, MovieSession
from django.db.models import QuerySet


def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        created_at = (
            datetime.fromisoformat(date) if date else None
        )
        order = Order.objects.create(
            user=user,
            created_at=created_at
        ) if created_at else Order.objects.create(user=user)
        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects
                .get(id=ticket["movie_session"]),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
        return order


def get_orders(username: str = None) -> QuerySet:
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs
