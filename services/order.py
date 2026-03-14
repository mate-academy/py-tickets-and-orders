from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession
from datetime import datetime
from typing import Optional
from django.db.models import QuerySet


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: Optional[str] = None, ) -> Order:
    user_u = get_user_model()
    user = user_u.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date is not None:
        dt_object = datetime.fromisoformat(date)
        Order.objects.filter(pk=order.pk).update(created_at=dt_object)
        order.refresh_from_db()

    for ticket in tickets:
        row = ticket["row"]
        seat = ticket["seat"]
        movie_session_id = ticket["movie_session"]
        movie_session = MovieSession.objects.get(pk=movie_session_id)
        Ticket.objects.create(movie_session=movie_session,
                              order=order,
                              row=row,
                              seat=seat)
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username).distinct()
    else:
        return Order.objects.all()
