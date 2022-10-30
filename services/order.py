from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket


def create_order(tickets: list, username: str, date: str = None) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        new_order = Order.objects.create(user=user)

        if date:
            new_order.created_at = date

        new_order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                order=new_order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"]
            )

        return new_order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
