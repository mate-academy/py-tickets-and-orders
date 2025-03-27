from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket, MovieSession


def create_order(tickets: list, username: User, date: str = None) -> None:
    user = User.objects.filter(username=username).first()
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            # Ticket.objects.create(order=order, **ticket)
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"])


def get_orders(username: str = None) -> Order | QuerySet[Order] | QuerySet:
    user = User.objects.filter(username=username).first()
    if username:
        return Order.objects.filter(user=user)
    return Order.objects.all()
