from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user_model = get_user_model()
    user = user_model.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        dt = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.objects.update(created_at=dt)
    for ticket in tickets:
        movie_session_pk = ticket.get("movie_session")
        movie_session = MovieSession.objects.get(pk=movie_session_pk)
        row = ticket.get("row")
        seat = ticket.get("seat")
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
