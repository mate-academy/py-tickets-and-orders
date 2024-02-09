from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User
from services.movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime.date = None
) -> None:
    user = User.objects.get(username=username)

    additional_order_data = {"user": user}

    order = Order.objects.create(**additional_order_data)

    if date:
        order.created_at = date

    order.save()

    ticket_objects = [
        Ticket(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=get_movie_session_by_id(
                ticket_data["movie_session"]
            ),
            order=order
        )
        for ticket_data in tickets
    ]

    Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
