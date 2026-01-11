from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(id=order.id).update(created_at=created_at)
        order.created_at = created_at
    for ticket_data in tickets:
        movie_session = (MovieSession
                         .objects
                         .get(id=ticket_data["movie_session"]))
        Ticket.objects.create(
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            order=order
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user).order_by("-created_at")
    return Order.objects.all().order_by("-created_at")
