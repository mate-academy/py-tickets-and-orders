from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        movie_session = MovieSession.objects.get(
            pk=ticket["movie_session"]
        )
        ticket = Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=movie_session,
            order=order
        )
        ticket.full_clean()
        ticket.save()
    return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
