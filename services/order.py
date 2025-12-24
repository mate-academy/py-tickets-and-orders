from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, MovieSession, Ticket
from datetime import datetime


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        movie_sessions_obj = MovieSession.objects.get(
            id=ticket["movie_session"])

        Ticket.objects.create(
            movie_session=movie_sessions_obj,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"])


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
