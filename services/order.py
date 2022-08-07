from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id


def create_order(tickets, username, date=None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=get_movie_session_by_id(ticket["movie_session"]),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username=None):
    orders = Order.objects.all().order_by("-id")

    if username:
        user = get_user_model().objects.get(username=username)
        orders = orders.filter(user_id=user.id)

    return orders
