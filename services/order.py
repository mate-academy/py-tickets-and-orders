from db.models import Order, Ticket
from django.db import transaction
from django.contrib.auth import get_user_model


def create_order(tickets: list, username: str, date=None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"]
            )


def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
