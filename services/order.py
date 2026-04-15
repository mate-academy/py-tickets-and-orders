from django.db import transaction
from db.models import Order, Ticket, MovieSession
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from django.contrib.auth import get_user_model

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    """
    tickets: list of dicts with keys: row, seat, movie_session
    username: str, user who creates the order
    date: optional str, sets created_at
    """
    user: User = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        created_at = parse_datetime(date)
        Order.objects.filter(id=order.id).update(created_at=created_at)
        order.refresh_from_db()

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
