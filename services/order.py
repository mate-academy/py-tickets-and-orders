from django.db import transaction

from db.models import Order
from db.models import Ticket


def create_order(tickets: list, username: str, date = None):
    with transaction.atomic():
        Order.objects.create(user=username)
        if date:
            Order.objects.get(user=username).created_at = date
        for i in tickets:
            Ticket.objects.create(movie_session=i.movie_session, order=Order.objects.get(user=username), row=i.row, seat=i.seat)

def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user=username)
    return Order.objects.all()
