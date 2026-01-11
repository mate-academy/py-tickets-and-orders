from db.models import Order
from db.models import User
from db.models import Ticket
from django.db import transaction
from db.models import MovieSession
from django.db.models import QuerySet


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for elem in tickets:
        movie_session = MovieSession.objects.get(id=elem["movie_session"])
        Ticket.objects.create(movie_session=movie_session,
                              row=elem["row"],
                              seat=elem["seat"],
                              order=order)
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
