from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        tickets_ = []
        user = get_user_model().objects.get(username=username)
        order = Order(user=user)
        if date:
            date_transform = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = date_transform
        else:
            order.created_at = datetime.now()
        order.save()
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            ticket_data = {
                "row": ticket["row"],
                "seat": ticket["seat"],
                "movie_session": movie_session,
                "order": order,
            }
            if not Ticket.objects.filter(**ticket_data).exists():
                ticket_ = Ticket(**ticket_data)
                tickets_.append(ticket_)

        if tickets_:
            Ticket.objects.bulk_create(tickets_)


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
