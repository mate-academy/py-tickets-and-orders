from django.db.models import QuerySet

from db.models import Ticket, Order, User
from django.db import transaction


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    name = User.objects.get(username=username)
    new_order = Order.objects.create(user=name)
    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        Ticket.objects.create(movie_session_id=ticket["movie_session"],
                              seat=ticket["seat"],
                              row=ticket["row"],
                              order=new_order)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
