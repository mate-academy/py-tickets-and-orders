from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    with transaction.atomic():
        order = Order(user=get_user_model().objects.get(username=username))
        if date:
            order.created_at = date
        order.save()

        for ticket_data in tickets:
            movie_session = ticket_data.get("movie_session")
            if isinstance(movie_session, int):
                try:
                    movie_session = MovieSession.objects.get(id=movie_session)
                except MovieSession.DoesNotExist:
                    raise ValueError(f"MovieSession with id "
                                     f"'{ticket_data['movie_session']}' "
                                     f"does not exist.")

            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket_data.get("row"),
                seat=ticket_data.get("seat")
            )

    return order
