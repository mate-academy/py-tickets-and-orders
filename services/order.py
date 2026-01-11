from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession
import datetime


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: datetime.datetime = None
) -> None:
    user = User.objects.get(username=username)

    order = Order.objects.create(
        user=user
    )
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return User.objects.get(username=username).orders.all()
    return Order.objects.all()
