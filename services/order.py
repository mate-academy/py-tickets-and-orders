
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User
from services.movie_session import get_movie_session_by_id


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session=get_movie_session_by_id(ticket["movie_session"]),
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
