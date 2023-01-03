from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=User.objects.get(username=username)
        )
        if date:
            new_order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            new_order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"],
                order=new_order
            )

    return new_order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(
            user_id=User.objects.get(username=username).id
        )
    return Order.objects.all()
