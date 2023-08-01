import datetime
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, User, Ticket
from services.movie_session import get_movie_session_by_id


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session=get_movie_session_by_id(
                    ticket["movie_session"]
                ),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(
        username: str = None
) -> QuerySet:
    if username:
        return Order.objects.filter(
            user__username=username
        )
    else:
        return Order.objects.all()
