from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:
    with transaction.atomic():
        check_user = User.objects.get(username=username)
        order = Order.objects.create(user=check_user)
        if date is not None:
            order.created_at = date
            order.save()
        for ticket in tickets:
            session = MovieSession.objects.get(id=ticket.get("movie_session"))
            Ticket.objects.create(order=order,
                                  movie_session=session,
                                  row=ticket.get("row"),
                                  seat=ticket.get("seat"))


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username).values_list()
    else:
        return Order.objects.all()
