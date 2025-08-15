from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(tickets: list, username: str, date: str = None) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            movie_session = ticket_data["movie_session"]
            if isinstance(movie_session, int):
                movie_session = MovieSession.objects.get(id=movie_session)
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(
            user=get_user_model().objects.get(username=username)
        )

    return Order.objects.all()
