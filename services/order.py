from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order
from db.models import Ticket
from db.models import MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

        Order.objects.filter(id=order.id).update(created_at=parsed_date)
        order.refresh_from_db()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket["movie_session"]
        )
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=movie_session
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
