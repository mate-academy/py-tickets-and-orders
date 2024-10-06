from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, MovieSession, Ticket


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    order.save()
    for ticket in tickets:
        movie_session = MovieSession.objects.get(pk=ticket["movie_session"])
        row = ticket["row"]
        seat = ticket["seat"]
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            seat=seat,
            row=row,
        )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
