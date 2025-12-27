import init_django_orm  # noqa: F401
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[Ticket],
        username: str,
        date: str = None,
) -> None:
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
        )
        if date:
            order.created_at = date
            order.save()

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


def get_orders(
        username: str = None,
) -> QuerySet[Ticket]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
