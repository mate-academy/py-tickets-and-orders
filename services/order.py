from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None) -> None:

    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(
            created_at=date,
            user=user
        )
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session_id = int(ticket["movie_session"])
            movie_session = MovieSession.objects.get(id=movie_session_id)
            print(movie_session)
            ticket = Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
