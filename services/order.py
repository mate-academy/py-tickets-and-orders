from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
    tickets: list[dict], username: str, date_created: datetime | str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date_created:
            order.created_at = date_created
            order.save()

        movie_sessions = {}

        for ticket in tickets:
            # Attempting to reduce number of DB calls a little.
            # For some reason I wasn't able to use `bulk_create()` here. :(
            if (session_id := ticket["movie_session"]) not in movie_sessions:
                movie_sessions[session_id] = MovieSession.objects.get(
                    id=session_id
                )

            Ticket.objects.create(
                movie_session=movie_sessions[session_id],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
