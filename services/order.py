from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession
from django.db import transaction


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)
        if date:
            new_order.created_at = date
            new_order.save()
        for ticket in tickets:
            movie_sessions = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie_sessions
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
