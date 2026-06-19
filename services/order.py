from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession
from django.db import transaction


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(order=order,
                                  row=ticket["row"],
                                  seat=ticket["seat"],
                                  movie_session=movie_session)
        if date:
            order.created_at = date
            order.save()


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders
