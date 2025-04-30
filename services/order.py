from datetime import datetime

from django.contrib.auth import get_user_model

from db.models import Order, Ticket, User, MovieSession
from django.db import transaction


def create_order(
    tickets: list,
    username: str,
    date: str = None,
) -> None:

    with transaction.atomic():

        order = Order.objects.create(
            user_id=User.objects.get(username=username).id
        )

        if date:
            not_str_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = not_str_date
            order.save()

        for ticket in tickets:

            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket.get("seat"),
            )


def get_orders(username: str = None) -> list:

    if username:
        return Order.objects.filter(
            user_id=get_user_model().objects.get(username=username).id
        ).all()

    return Order.objects.all()
