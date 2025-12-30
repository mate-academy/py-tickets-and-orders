from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User, MovieSession


def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[datetime] = None) -> Order:
    with (((transaction.atomic()))):
        user = User.objects.get(username=username)
        order = Order(user=user)
        order.save()  # 🟢 Тут created_at запишеться автоматично

        if date is not None:
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            Order.objects.filter(pk=order.pk).update(created_at=date)
            order.created_at = date

        for ticket in tickets:
            ticket_id = ticket["movie_session"]
            movie_session = MovieSession.objects.get(id=ticket_id)

            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"]
            )

        return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username__iexact=username)
    return Order.objects.all()
