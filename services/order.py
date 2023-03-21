from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            new_order.created_at = date
            new_order.save()
        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket_data["movie_session"]),
                order=new_order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
