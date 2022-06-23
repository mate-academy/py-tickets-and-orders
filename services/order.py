from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(tickets, username, date=None):

    with transaction.atomic():
        customer = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=customer)

        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order)


def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
