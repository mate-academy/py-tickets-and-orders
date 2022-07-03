from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, MovieSession, Ticket


def create_order(tickets: list, username: str, date=None):
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
            Ticket.objects.create(movie_session=movie_session,
                                  order=order,
                                  row=ticket["row"],
                                  seat=ticket["seat"])


def get_orders(username: str = None):
    result = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        result = Order.objects.filter(user_id=user.id)
    return result
