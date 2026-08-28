from django.db.models import QuerySet
from db.models import Ticket, User, Order, MovieSession
from django.db import transaction
from typing import Optional


@transaction.atomic
def create_order(username: str, tickets: list,
                 date: Optional[str] = None) -> Order:
    user = User.objects.get(username=username)

    order = Order(user=user)
    order.save()
    if date:
        Order.objects.filter(pk=order.pk).update(created_at=date)
    for ticket in tickets:
        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return (Order.objects.filter(user__username=username))
    return (Order.objects.all())
