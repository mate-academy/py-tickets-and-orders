from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            new_order.created_at = date
            new_order.save()
        for ticket in tickets:
            session = MovieSession.objects.get(pk=ticket["movie_session"])
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=session,
                order=new_order
            )


def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
