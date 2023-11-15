from db.models import Ticket, Order, User, MovieSession
from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"],
                order=order,
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username__icontains=username)
    return Order.objects.all()
