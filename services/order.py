from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession
from django.db import transaction
from datetime import datetime


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None,
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
            row=ticket["row"],
            seat=ticket["seat"]
        )

    order.save()
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders
