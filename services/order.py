from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        new_order = Order.objects.create(
            user=user
        )
        if date:
            new_order.created_at = date

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            new_ticket = Ticket.objects.create(
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"],
                order=new_order
            )
            new_ticket.save()

        new_order.save()


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username).id
        return Order.objects.filter(user_id=user)
    return Order.objects.all()
