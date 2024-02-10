
from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order
from datetime import datetime


def create_order(tickets: list[Ticket], username: str,
                 date: str = None) -> None:
    user = get_user_model().objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(created_at=date, user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()
        for ticket in tickets:
            Ticket.objects.create(movie_session_id=ticket["movie_session"],
                                  order=order,
                                  row=ticket["row"], seat=ticket["seat"])


def get_orders(username: str = None) -> list[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
