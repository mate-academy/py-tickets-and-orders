from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from django.contrib.auth import get_user_model


User = get_user_model()


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        created_at = datetime.strptime(
            date, "%Y-%m-%d %H:%M"
        ) if date else None

        order = Order.objects.create(user=user)
        if created_at:
            order.created_at = created_at
            order.save(update_fields=["created_at"])

        for ticket_data in tickets:
            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"],
                order=order
            )

        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
