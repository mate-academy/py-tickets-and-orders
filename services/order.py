from django.db import transaction
from db.models import Ticket
from db.models import User
from db.models import Order
from db.models import MovieSession


def create_order(tickets: list, username: str, date: str = None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user_id=user.id)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None):
    order = Order.objects.all().order_by("-user")
    if username:
        order = order.filter(user__username=username)
    return order
