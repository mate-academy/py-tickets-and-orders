from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


def create_order(tickets, username, date=None):
    with transaction.atomic():
        created_order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

        if date:
            created_order.created_at = date

        created_order.save()

        for ticket in tickets:
            row, seat, movie_session = ticket.values()
            Ticket.objects.create(
                movie_session_id=movie_session,
                order=created_order,
                row=row,
                seat=seat)


def get_orders(username=None):
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
