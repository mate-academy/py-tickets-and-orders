from typing import List

from django.db import transaction

from db.models import Ticket, Order, User, MovieSession


@transaction.atomic
def create_order(
        tickets: List[dict],
        username: str,
        date: str = None
) -> None:
    user_instance = User.objects.get(username=username)

    order_instance = (Order.objects.create(user=user_instance))

    if date:
        order_instance.created_at = date
        order_instance.save()

    for ticket_data in tickets:
        movie_session_instance = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )

        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=movie_session_instance,
            order=order_instance)

    return order_instance


def get_orders(username: str = None) -> Order:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
