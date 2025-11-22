from django.db import transaction
from django.db.models import QuerySet

from db.models import Order
from db.models import Ticket


def create_order(tickets: list, username: str, date = None):
    with transaction.atomic():
        Order.objects.create(user=username)
        if date:
            Order.objects.get(user=username).created_at = date
        for i in tickets:
            Ticket.objects.create(movie_session__id=i["movie_session"], order=Order.objects.get(user=username), row=i["row"], seat=i["seat"])

def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
