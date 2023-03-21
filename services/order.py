from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket_dict in tickets:
            Ticket.objects.create(
                row=ticket_dict["row"],
                seat=ticket_dict["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket_dict["movie_session"]
                ),
                order=order)


def get_orders(username: str = None) -> QuerySet:
    query_set = Order.objects.all()
    if username:
        query_set = query_set.filter(user__username=username)
    return query_set
