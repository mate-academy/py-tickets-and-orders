from django.db.models import QuerySet

from typing import List

from django.contrib.auth import get_user_model

from django.db import transaction

from db.models import Order, Ticket, MovieSession


def create_order(tickets: List[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                movie_session=MovieSession.objects.get(
                    pk=ticket_data.get("movie_session")
                ),
                row=ticket_data.get("row"),
                seat=ticket_data.get("seat")
            )


def get_orders(username: str = None) -> QuerySet:
    with transaction.atomic():
        if username:
            user = get_user_model().objects.get(username=username)
            return Order.objects.filter(user=user)
        else:
            return Order.objects.all()
