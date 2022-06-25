from db.models import Order, Ticket
from django.contrib.auth import get_user_model
from django.db import transaction


def create_order(tickets: list, username, date=None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)

        order = Order.objects.create(user=user)
        print(order)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"])


def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
