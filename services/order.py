import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(tickets: list[dict],
                 username: User,
                 date: datetime.datetime = None) -> Order:
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            tick = Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order)
            tick.save()
        return order


def get_orders(username: User = None) -> QuerySet:
    order = Order.objects.all().order_by("-created_at").values_list("id")
    if username:
        order = order.filter(user__username=username)

    return order
