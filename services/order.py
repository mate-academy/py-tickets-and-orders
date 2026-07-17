from django.db.models import QuerySet
from datetime import datetime
from db.models import Order, Ticket, User, MovieSession
from django.db import transaction


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            Order.objects.filter(
                pk=order.pk).update(
                created_at=datetime.strptime(date, "%Y-%m-%d %H:%M"))
        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]), order=order)


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
