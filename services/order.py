import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    user_obj = User.objects.get(username=username)
    with transaction.atomic():
        order_obj = Order.objects.create(user_id=user_obj.id)
        if date:
            order_obj.created_at = date
            order_obj.save()

        ticket_objs = [
            Ticket(
                movie_session=MovieSession.objects.get(
                    id=ticket_data["movie_session"]
                ),
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                order_id=order_obj.id
            ) for ticket_data in tickets
        ]
        Ticket.objects.bulk_create(ticket_objs)


def get_orders(username: str = None) -> QuerySet:
    if username:
        user_obj = User.objects.get(username=username)
        return Order.objects.filter(user_id=user_obj.id)
    return Order.objects.all()
