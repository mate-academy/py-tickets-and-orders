from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()

        ticket_objects = [
            Ticket(
                order=order,
                movie_session=get_movie_session_by_id
                (movie_session_id=ticket["movie_session"]),
                row=ticket["row"],
                seat=ticket["seat"]
            ) for ticket in tickets
        ]

        Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
