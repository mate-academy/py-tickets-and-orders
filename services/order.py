from db.models import Order, Ticket, User
from django.db import transaction
from datetime import datetime


def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(
            user=user,
            created_at=datetime.fromisoformat(date) if date else datetime.now()
        )
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
            )
        return order


def get_orders(username: str = None) -> list:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
