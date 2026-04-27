import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: dict,
        username: str,
        date: datetime.datetime = None) -> None:
    order = Order.objects.create(user=get_user_model()
                                 .objects.get_or_create(username=username)[0])
    if date:
        order.created_at = date
    order.save(update_fields=["created_at"])
    list_of_tickets = [Ticket(movie_session_id=ticket["movie_session"],
                              order=order,
                              row=ticket["row"],
                              seat=ticket["seat"]) for ticket in tickets]
    for i in list_of_tickets:
        i.clean()
    Ticket.objects.bulk_create(list_of_tickets)


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
