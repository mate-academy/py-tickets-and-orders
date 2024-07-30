from datetime import datetime

from django.contrib.auth import get_user_model

from django.db import transaction

from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list[Ticket],
        username: str | User,
        date: datetime = None
) -> Order:
    with transaction.atomic():
        users = get_user_model().objects.get(username=username)
        order_data = {"user": users}
        Order.objects.create(**order_data)
        if date:
            order_data["created_at"] = date
            Order.objects.update(**order_data)

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            order = Order.objects.get(id=ticket["movie_session"])
            ticket_data = Ticket.objects.create(
                seat=ticket["seat"],
                row=ticket["row"],
                movie_session=movie_session,
                order=order,
            )

    return ticket_data


def get_orders(username: str = None) -> QuerySet:
    if username:
        return (Order.objects.filter
                (user__username=username).order_by("-created_at"))

    return Order.objects.all().order_by("-created_at")
