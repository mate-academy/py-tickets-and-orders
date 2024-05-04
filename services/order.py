from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str, date: str | None = None) -> None:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    movie_session_ids = set(ticket_data["movie_session"]
                            for ticket_data in tickets)

    movie_sessions = {
        movie_session.id: movie_session
        for movie_session
        in MovieSession.objects.filter(id__in=movie_session_ids)
    }

    ticket_instances = [
        Ticket(
            movie_session=movie_sessions[ticket_data["movie_session"]],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
        for ticket_data in tickets
    ]

    Ticket.objects.bulk_create(ticket_instances)


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
