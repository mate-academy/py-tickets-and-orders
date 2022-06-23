from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


def create_order(tickets, username, date=None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user_id=user.id)

        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            session = MovieSession.objects.get(id=ticket["movie_session"])
            Ticket.objects.create(
                movie_session=session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"])


def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
