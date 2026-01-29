from django.contrib.auth import get_user_model

from django.db import transaction
from db.models import Order, MovieSession, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    ticket_data = None

    for ticket in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket["movie_session"]
        )

        ticket_data = Ticket.objects.create(
            seat=ticket["seat"],
            row=ticket["row"],
            movie_session=movie_session,
            order=order,
        )

    return ticket_data


def get_orders(
        username: str = None
) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
