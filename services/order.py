from django.contrib.auth import get_user_model
from django.db import transaction
from typing import Optional
from db.models import Order, Ticket, MovieSession
from django.db.models import QuerySet


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None
) -> QuerySet:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()
        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )
            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=movie_session,
                order=order
            )

        return order


def get_orders(
        username: Optional[str] = None,
) -> QuerySet:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
