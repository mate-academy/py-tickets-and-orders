from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, MovieSession, Ticket


def create_order(tickets: list, username: str, date: str = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            movie_session_id = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session_id,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
