import init_django_orm  # noqa: F401

from django.db import transaction

from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)

        created_order = Order.objects.create(user=user)

        if date:
            created_order.created_at = date
            created_order.save()

        for ticket in tickets:
            row, seat, movie_session = ticket.values()

            Ticket.objects.create(
                movie_session_id=movie_session,
                order_id=created_order.id,
                row=row,
                seat=seat
            )


def get_orders(username: str = None) -> QuerySet:
    query = Order.objects.all()

    if username:
        query = query.filter(user__username=username)

    return query
