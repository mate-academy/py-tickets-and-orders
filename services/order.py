from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order
from services.movie_session import get_movie_session_by_id


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> None:
    with transaction.atomic():
        new_order = Order()
        new_order.user = get_user_model().objects.get(username=username)

        if date:
            new_order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")

        new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=new_order,
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session=get_movie_session_by_id(
                    ticket.get("movie_session")
                )
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
