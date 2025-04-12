from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, User, Order, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user, created_at=date)

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)

    return Order.objects.all()
