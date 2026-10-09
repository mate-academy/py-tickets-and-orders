from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, MovieSession, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        Order.objects.filter(pk=order.pk).update(
            created_at=datetime.strptime(date, "%Y-%m-%d %H:%M")
        )
        order.refresh_from_db()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(pk=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = Order.objects.filter(user__username=username)

    return queryset
