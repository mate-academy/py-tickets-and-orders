from django.db import transaction

from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model


def create_order(tickets, username, date=None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        user_id = user.id
        order = Order.objects.create(user_id=user_id)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"])


def get_orders(username=None):
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user_id=user.id)
    return Order.objects.all()
