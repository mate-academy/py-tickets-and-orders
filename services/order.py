from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, MovieSession, Ticket


def create_order(tickets: list,
                 username: str,
                 date: str = None) -> None:
    user = get_user_model()
    with transaction.atomic():
        user, _ = user.objects.get_or_create(username=username)
        order = Order.objects.create(
            user=user,
            created_at=date,
        )
        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet[Order] | QuerySet[None]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
