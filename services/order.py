from db.models import Order

from django.db.models import QuerySet

from db.models import User

from django.db import transaction

from db.models import Ticket

from db.models import MovieSession

from datetime import datetime


def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None
) -> QuerySet:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for value in tickets:
            movie = MovieSession.objects.get(id=value["movie_session"])
            Ticket.objects.create(
                row=value["row"],
                seat=value["seat"],
                movie_session=movie,
                order=order
            )
        return order


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user.id)
    return Order.objects.all()
