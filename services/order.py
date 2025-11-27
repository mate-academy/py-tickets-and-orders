from django.db.models import QuerySet
import datetime
from django.db import transaction
from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None
) -> None:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Exception("Username not found")
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            movie_sessions_obj = MovieSession.objects.get(
                id=ticket["movie_session"])
            Ticket.objects.create(
                movie_session=movie_sessions_obj,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"])


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(
            user__username=username).order_by("-created_at")
    return Order.objects.all().order_by("-created_at")
