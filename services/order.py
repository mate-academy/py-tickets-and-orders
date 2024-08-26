from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import MovieSession, Order, Ticket, User


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    for ticket_data in tickets:
        movie_session_id = ticket_data["movie_session"]
        row = ticket_data["row"]
        seat = ticket_data["seat"]

        movie_session = MovieSession.objects.get(id=movie_session_id)

        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=row,
            seat=seat
        )

    if date:
        created_at = parse_datetime(date)
        if created_at:
            order.created_at = created_at
            order.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
