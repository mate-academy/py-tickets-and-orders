from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = parse_datetime(date)
            order.save()
        for ticket in tickets:
            movie_session_obj = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            if Ticket.objects.filter(
                    movie_session=movie_session_obj,
                    row=ticket["row"],
                    seat=ticket["seat"]
            ).exists():
                raise ValidationError(
                    f"Seat {ticket['row']}-{ticket['seat']} is already taken "
                    f"for session {movie_session_obj.id}."
                )
            Ticket.objects.create(
                movie_session=movie_session_obj,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
