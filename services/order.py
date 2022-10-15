from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(tickets: dict, username, date=None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order_ = Order.objects.create(user=user)
        if date:
            order_.created_at = date
            order_.save()
        [
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                order=order_,
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"])
            ) for ticket in tickets
        ]


def get_orders(username=None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all().order_by("-id")
