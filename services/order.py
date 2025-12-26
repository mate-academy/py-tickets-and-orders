from db.models import Order, Ticket, User, MovieSession
from django.db import transaction
from django.db.models import QuerySet
import datetime


def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session_id = ticket.pop("movie_session")
            movie_session = MovieSession.objects.get(pk=movie_session_id)
            Ticket.objects.create(order=order,
                                  movie_session=movie_session,
                                  **ticket)
        return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        user = User.objects.get(username=username)
        orders = Order.objects.filter(user=user)
    return orders
