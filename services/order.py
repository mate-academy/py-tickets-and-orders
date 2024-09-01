from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession, User


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        orders = Order.objects.filter(user=user)
    else:
        orders = Order.objects.all()
    return orders
