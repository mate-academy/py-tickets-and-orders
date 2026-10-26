from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import MovieSession, Order, Ticket


def _prepare_date(date: str | datetime) -> datetime:
    if isinstance(date, datetime):
        return date

    parsed_date = parse_datetime(date)

    if parsed_date is not None:
        return parsed_date

    return datetime.strptime(date, "%Y-%m-%d %H:%M")


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | datetime = None,
) -> Order:
    user_model = get_user_model()
    user = user_model.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = _prepare_date(date)
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )

        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=movie_session,
            order=order,
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
