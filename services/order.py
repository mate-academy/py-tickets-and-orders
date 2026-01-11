from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        raise ValueError(f"There is no user with username '{username}'")

    order = Order.objects.create(user=user)

    tickets = [
        Ticket(
            order=order,
            row=data["row"],
            seat=data["seat"],
            movie_session=MovieSession.objects.get(id=data["movie_session"])
        )
        for data in tickets
    ]

    if date:
        order.created_at = date
        order.save()

    Ticket.objects.bulk_create(tickets)
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
