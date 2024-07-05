from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import MovieSession, Order, User, Ticket


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    pk=ticket["movie_session"]
                ),
                order=order
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username__exact=username)
    else:
        return Order.objects.all()
