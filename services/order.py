from datetime import datetime

from django.db import transaction

from db.models import Ticket, Order, User, MovieSession


def create_order(  # s/4
        tickets: list[dict],
        username: str,
        date: datetime = None,
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                )
            )

    return order


def get_orders(
        username: str = None
) -> Order:
    if username:
        return Order.objects.filter(
            user__username=username
        )
    return Order.objects.all()
