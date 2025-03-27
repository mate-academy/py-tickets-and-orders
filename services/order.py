from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        new_order = Order.objects.create(user=user)
        if date:
            new_order.created_at = date

        for ticket in tickets:
            movie_sessions = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_sessions,
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )

        return new_order


def get_orders(
        username: str = None,
) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
