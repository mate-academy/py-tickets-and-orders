from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(tickets: list, username: str, date: int = None) -> list[dict]:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session_id=ticket.get("movie_session")
            )
    return order


def get_orders(username: str = None) -> list:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
