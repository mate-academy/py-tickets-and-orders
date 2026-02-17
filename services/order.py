from django.db import transaction
from django.utils.dateparse import parse_datetime

from db.models import Order, MovieSession, Ticket
from django.contrib.auth import get_user_model


def create_order(tickets: list, username: str, date: str = None) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            parsed_date = parse_datetime(date)
            if parsed_date is None:
                raise ValueError("Invalid date format. Use 'YYYY-MM-DD HH:MM'")
            order.created_at = parsed_date
            order.save(update_fields=["created_at"])

        for tic in tickets:
            movie_session = MovieSession.objects.get(pk=tic["movie_session"])
            ticket = Ticket(
                order=order,
                movie_session=movie_session,
                row=tic["row"],
                seat=tic["seat"]
            )
            ticket.save()

        return order


def get_orders(username: str = None) -> Order:
    result = Order.objects.all()
    if username:
        result = result.filter(user__username=username)
    return result
