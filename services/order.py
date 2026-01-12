from datetime import datetime

from django.db import transaction

from db.models import Ticket, Order, User


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username),
        )

        if date:
            order.created_at = date

        for ticket in tickets:
            ticket_obj = Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order)
            ticket_obj.save()

        order.save()

        return order


def get_orders(username: str = None) -> list:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user=User.objects.get(username=username))
    return queryset
