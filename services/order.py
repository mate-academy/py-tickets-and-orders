from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(
            user=user
        )

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            row, seat, movie_session = ticket_data.values()
            movie_session = MovieSession.objects.get(id=movie_session)

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=row,
                seat=seat
            )


def get_orders(
        username: str = None,
) -> QuerySet:
    return Order.objects.filter(
        user__username=username
    ) if username else Order.objects.all()
