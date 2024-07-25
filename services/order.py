from db.models import Order, User, Ticket, MovieSession
from django.db import transaction
import datetime


def create_order(
        tickets: list,
        username: str,
        date: datetime.datetime = None
) -> None:
    user = User.objects.get(username=username)
    created_at = date if date else None

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=created_at)

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(id=ticket_data['movie_session'])
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket_data['row'],
                seat=ticket_data['seat']
            )


def get_orders(username: str = None) -> list:
    query = Order.objects.all()

    if username:
        user = User.objects.get(username=username)
        query = query.filter(user=user)

    return query
