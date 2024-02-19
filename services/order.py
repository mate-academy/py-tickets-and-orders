from datetime import datetime

from django.db import transaction

from django.contrib.auth import get_user_model

from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None,
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(
            user=user)
        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            row = ticket["row"]
            seat = ticket["seat"]
            movie_session_id = ticket["movie_session"]

            Ticket.objects.create(
                order=order,
                row=row,
                seat=seat,
                movie_session_id=movie_session_id
            )


def get_orders(username: str = None) -> QuerySet:
    if username is None:
        return Order.objects.all()

    user_model = get_user_model()
    user = user_model.objects.get(username=username)
    return Order.objects.filter(user=user)
