from db.models import Ticket
from db.models import Order
from db.models import User
from django.db.models import QuerySet

from django.db import transaction


def create_order(
        tickets: dict,
        username: str,
        date: str = None) -> None:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            ticket = Ticket(
                movie_session_id=ticket_data["movie_session"],
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
            ticket.full_clean()
            ticket.save()


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
