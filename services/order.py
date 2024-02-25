from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, MovieSession, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            if ticket["movie_session"]:
                movie_session = MovieSession.objects.get(
                    pk=ticket["movie_session"]
                )
                ticket["movie_session"] = movie_session

            Ticket.objects.create(order=order, **ticket)
        return order


def get_orders(username: str = None) -> list[dict]:
    order = Order.objects.all()
    if username:
        return order.filter(user__username=username)
    return order
