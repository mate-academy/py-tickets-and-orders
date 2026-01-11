from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str, date:
        datetime = None
) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise User.DoesNotExist
    order = Order.objects.create(user_id=user.id)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        try:
            MovieSession.objects.get(id=ticket["movie_session"])
        except MovieSession.DoesNotExist:
            raise MovieSession.DoesNotExist
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(
            user__username=username
        ).order_by("-created_at")
    else:
        return Order.objects.all().order_by("-created_at")
