from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)

        order = Order.objects.create(user=user)
        if date:
            created_at = timezone.datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = created_at
            order.save()

        for ticket_data in tickets:
            row = ticket_data.get("row")
            seat = ticket_data.get("seat")
            movie_session_id = ticket_data.get("movie_session")

            movie_session = MovieSession.objects.get(pk=movie_session_id)

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=row,
                seat=seat,
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
