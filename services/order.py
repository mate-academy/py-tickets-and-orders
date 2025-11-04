from datetime import datetime

from django.db import transaction

from db.models import Order
from db.models import Ticket
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from services.movie_session import get_movie_session_by_id


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None,
                 ) -> None:
    user_object = get_user_model().objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(
            user=user_object
        )
        if date:
            parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = parsed_date
            order.save(update_fields=["created_at"])

        for ticket in tickets:
            movie_session = get_movie_session_by_id(ticket["movie_session"])
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        user_object = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user_object)
    return Order.objects.all()
