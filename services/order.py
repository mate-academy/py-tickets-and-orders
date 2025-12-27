from datetime import datetime
from django.db import transaction

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    if not get_user_model().objects.filter(username=username).exists():
        user = get_user_model().objects.create_user(username=username)
    else:
        user = get_user_model().objects.get(username=username)

    order = Order(user=user)
    order.save()

    if date:
        datetime_obj = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(pk=order.id).update(created_at=datetime_obj)

    for ticket in tickets:
        row = ticket.get("row")
        seat = ticket.get("seat")
        movie_session = MovieSession.objects.get(
            pk=ticket.get("movie_session")
        )

        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
