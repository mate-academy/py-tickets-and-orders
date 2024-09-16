from django.db import transaction

import db.models
from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list, username: str, date: str = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(
                username=username
            )
        )

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    pk=ticket["movie_session"]
                )
            )


def get_orders(username: str = None) -> db.models.Order:
    users_order = Order.objects.filter(user__username=username)
    if users_order:
        return users_order
    return Order.objects.all()
