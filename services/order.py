from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(
            user=user
        )
        if date:
            order.created_at = date
            order.save()
        ticket_data = []
        for ticket in tickets:
            ticket_movie_session = ticket["movie_session"]
            movie_session = MovieSession.objects.get(id=ticket_movie_session)
            ticket = Ticket(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie_session
            )
            ticket_data.append(ticket)

        Ticket.objects.bulk_create(ticket_data)


def get_orders(username: str = None) -> QuerySet:
    if username:
        user_id = User.objects.get_by_natural_key(username=username).id
        return Order.objects.filter(user_id=user_id).values()
    else:
        return Order.objects.all()
