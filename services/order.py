from typing import Optional

from django.contrib.auth import get_user_model

from django.db import transaction

from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None,
) -> None:
    with transaction.atomic():
        user_to_add = User.objects.get(username=username)
        new_order = Order.objects.create(user=user_to_add)
        if date:
            new_order.created_at = date
            new_order.save()

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                order=new_order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
            )


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        queryset = queryset.filter(user=user)

    return queryset
