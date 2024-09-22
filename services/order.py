from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from services.movie_session import get_movie_session_by_id

user = get_user_model()


def create_order(tickets: list[dict], username: str, *,
                 date: str = None) -> None:
    with transaction.atomic():
        try:
            user_received = user.objects.get(username=username)
            user_data = {"user": user_received}
            if date:
                user_data["created_at"] = date
            order = Order.objects.create(**user_data)

            ticket_objects = []
            for ticket in tickets:
                try:
                    get_movie_session_by_id(ticket["movie_session"])
                except MovieSession.DoesNotExist:
                    raise ValueError(
                        f"MovieSession with id {ticket['movie_session']} "
                        "does not exist")

                ticket_objects.append(
                    Ticket(
                        seat=ticket["seat"],
                        row=ticket["row"],
                        movie_session_id=ticket["movie_session"],
                        order=order
                    )
                )

            Ticket.objects.bulk_create(ticket_objects)
        except user.DoesNotExist:
            raise ValueError(f"User {username} does not exist")


def get_orders(*, username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user=user.objects.get(username=username))
    return queryset
