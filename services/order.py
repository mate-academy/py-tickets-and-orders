from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(
        tickets: list,
        username: str,
        date: str = '',
) -> None:

    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order()

        order.user = user
        if date:
            parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = parsed_date  # <-- Ключова зміна

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
