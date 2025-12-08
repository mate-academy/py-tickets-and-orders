from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order.objects.create(user=user)
        order.created_at = created_at
        order.save(update_fields=["created_at"])
    else:
        order = Order.objects.create(user=user)

    for ticket in tickets:
        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
