from django.db.models import QuerySet
from db.models import Ticket, Order, MovieSession
from django.db import transaction
import datetime
from django.contrib.auth import get_user_model
User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> Order:
    user = (get_user_model().
            objects.get(username=username))
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(pk=ticket["movie_session"],)
        Ticket.objects.create(movie_session=movie_session,
                              order=order,
                              row=ticket["row"],
                              seat=ticket["seat"],)
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
