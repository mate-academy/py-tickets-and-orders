from django.db import transaction

import init_django_orm  # noqa: F401
from db.models import MovieSession
from db.models import Ticket
from db.models import Order
from db.models import User


def create_order(tickets: list, username, date=None):
    user_ = User.objects.get(username=username)
    with transaction.atomic():
        order_ = Order.objects.create(
            created_at=date, user=user_)
        if date:
            order_.created_at = date
            order_.save()
        for ticket in tickets:
            movie_session_ = MovieSession.objects.get(
                id=ticket["movie_session"])
            Ticket.objects.create(
                movie_session=movie_session_,
                order_id=order_.id,
                row=ticket["row"],
                seat=ticket["seat"])


def get_orders(username=None):
    if username:
        user_ = User.objects.get(username=username)
        return Order.objects.filter(user_id=user_.id)
    return Order.objects.all()
