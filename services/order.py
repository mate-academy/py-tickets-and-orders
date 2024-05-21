import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            pk=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
    if date:
        order.created_at = date
        order.save()
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = Order.objects.filter(user__username=username)
    return orders
