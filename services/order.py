from django.db import transaction

from db.models import Order, Ticket, User


def create_order(tickets: list, username:str, date: str=None):
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(row=ticket["row"], seat=ticket["seat"], order=order, movie_session_id=ticket["movie_session"])


def get_orders(username: str=None):
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))
    return Order.objects.all()