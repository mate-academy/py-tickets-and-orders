from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, MovieSession, Ticket


def create_order(
    tickets: list[dict], username: str, date: datetime = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        ticket_instances = []

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            row = ticket_data["row"]
            seat = ticket_data["seat"]
            movie_session_id = ticket_data["movie_session"]
            movie_session = MovieSession.objects.get(movie_id=movie_session_id)

            ticket = Ticket(
                movie_session=movie_session, order=order, row=row, seat=seat
            )
            ticket_instances.append(ticket)

        Ticket.objects.bulk_create(ticket_instances)

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
