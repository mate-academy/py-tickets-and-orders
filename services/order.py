from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)

    params = {"user": user}
    if date:
        params["created_at"] = date

    order = Order.objects.create(**params)

    for tick in tickets:
        ticket = Ticket(
            row=tick["row"],
            seat=tick["seat"],
            movie_session_id=tick["movie_session"],
            order=order,
        )
        ticket.full_clean()
        ticket.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
