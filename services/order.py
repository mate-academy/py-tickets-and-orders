from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = User.objects.filter(username=username).first()
    order = Order(user=user)
    if date:
        order.created_at = date
    order.save()

    for ticket in tickets:
        Ticket.objects.create(row=ticket["row"],
                              seat=ticket["seat"],
                              movie_session_id=ticket["movie_session"],
                              order=order)


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
