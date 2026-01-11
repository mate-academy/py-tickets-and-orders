from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import MovieSession, Order, Ticket


def create_order(
    tickets: list[dict],
    username: str,
    date: datetime | None = None,
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            ticket = Ticket(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
            movie_session = MovieSession.objects.get(
                pk=ticket_data["movie_session"]
            )
            ticket.movie_session = movie_session
            ticket.save()

        return order


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
