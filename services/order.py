from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User
from db.models import Ticket


@transaction.atomic()
def create_order(tickets: list, username: str, date = None):
    if date:
        Order.objects.create(user=User.objects.get(username=username), created_at=date)
    Order.objects.create(user=User.objects.get(username=username))
    order = Order.objects.get(user=username)
    for i in tickets:
        Ticket.objects.create(movie_session__id=i["movie_session"], order=order, row=i["row"], seat=i["seat"])

def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
