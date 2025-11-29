from django.db.models import QuerySet
from db.models import Order, Ticket
from django.db import transaction
from datetime import datetime
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
        date: datetime = None) -> None:

    user = get_user_model().objects.get(username=username)

    order_data = {"user": user}
    order = Order.objects.create(**order_data)
    if date:
        order.created_at = date
    order.save()

    ticket_objects = [
        Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order,
        )
        for ticket in tickets
    ]
    # Ticket.objects.bulk_create(ticket_objects)
    for ticket in ticket_objects:
        ticket.save()


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
