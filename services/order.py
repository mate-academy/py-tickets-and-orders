from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession
from datetime import datetime

User = get_user_model()


def _parse_date(date: str) -> datetime:
    formats = ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M")
    for fmt in formats:
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            continue
    raise ValueError(f"unknown date format: {date!r}")


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:

        if isinstance(date, str):
            order.created_at = _parse_date(date)
            order.save(update_fields=["created_at"])

    for ticket in tickets:
        ms = MovieSession.objects.get(pk=ticket["movie_session"])
        Ticket.objects.create(movie_session=ms,
                              order=order,
                              row=ticket["row"],
                              seat=ticket["seat"])
    return order


def get_orders(username: str = None) -> list:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
