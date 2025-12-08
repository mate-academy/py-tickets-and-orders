from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order(user=user)
    order.save()
    if date:
        (Order.objects.filter(id=order.id)
         .update(created_at=datetime.strptime(date, "%Y-%m-%d %H:%M")))
    for ticket in tickets:
        session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
