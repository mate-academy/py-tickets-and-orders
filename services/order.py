from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)
        if date:
            created_at_format = datetime.strptime(date, "%Y-%m-%d %H:%M")
            new_order.created_at = created_at_format
            new_order.save()

        for ticket_data in tickets:
            row, seat, movie_session_id = ticket_data.values()
            Ticket.objects.create(
                order=new_order,
                row=row,
                seat=seat,
                movie_session_id=movie_session_id,
            )
        return new_order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        user = get_user_model().objects.get(username=username)
        return queryset.filter(user=user)
    return queryset
