import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from services.movie_session import get_movie_session_by_id

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None
) -> None:
    user = get_user_model().objects.get(username=username)
    new_order = Order.objects.create(user=user)

    if date is not None:
        new_order.created_at = date
        new_order.save(update_fields=["created_at"])

    session_ids = {ticket["movie_session"] for ticket in tickets}
    sessions = MovieSession.objects.in_bulk(session_ids)

    tickets_to_create = [
        Ticket(
            order=new_order,
            movie_session=sessions[ticket["movie_session"]],
            row=ticket["row"],
            seat=ticket["seat"]
        )
        for ticket in tickets
    ]

    Ticket.objects.bulk_create(tickets_to_create)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
