from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order, User
from datetime import datetime


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> Order:
    user = User.objects.get(username=username)
    new_order = Order.objects.create(
        user=user,
    )
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=new_order,
        )
    if date:
        new_order.created_at = date
    new_order.save()
    return new_order


def get_orders(username: str = None) -> Order | QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
