from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


def create_order(
    tickets: list[Ticket], username: str, date: str = None
) -> Order:
    with transaction.atomic():
        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create(username=username)

        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            row = ticket_data["row"]
            seat = ticket_data["seat"]
            movie_session_id = ticket_data["movie_session"]

            movie_session = MovieSession.objects.get(id=movie_session_id)

            Ticket.objects.create(
                row=row,
                seat=seat,
                movie_session=movie_session,
                order=order,
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
