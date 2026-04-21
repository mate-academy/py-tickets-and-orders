from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket

@transaction.atomic
def create_order(tickets: list, username:str, date: str=None) -> Order:
    order = Order.objects.create(user=get_user_model().objects.get(username=username))
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(row=ticket["row"], seat=ticket["seat"], order=order, movie_session_id=ticket["movie_session"])
    return order


def get_orders(username: str=None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()