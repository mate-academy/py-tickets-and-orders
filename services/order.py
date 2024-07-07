from datetime import datetime

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, User
from services.movie_session import get_movie_session_by_id


def create_order(tickets: list,
                 username: str,
                 date: datetime = None
                 ) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        ticket_order = [
            Ticket(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=get_movie_session_by_id(
                    movie_session_id=ticket["movie_session"]
                ),
                order=order
            )
            for ticket in tickets
        ]
        order.save()
        Ticket.objects.bulk_create(ticket_order)
        return order


def get_orders(username: User = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
