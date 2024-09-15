from django.db.models import QuerySet
from django.db import transaction

from db.models import Order, User, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    order.save()
    for ticket in tickets:
        movie_session_id = ticket.get("movie_session")
        movie_session = MovieSession.objects.get(id=movie_session_id)

        Ticket.objects.create(
            row=ticket.get("row"),
            seat=ticket.get("seat"),
            movie_session=movie_session,
            order=order
        )


def get_orders(
        username: str = None,
) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
