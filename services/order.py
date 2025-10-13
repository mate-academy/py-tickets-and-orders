from typing import List, Dict, Union
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession
from services.user import get_user

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: List[Dict[str, Union[int, str]]],
    username: str,
    date: Union[str, "datetime.datetime"] = None,
) -> Order:
    user = User.objects.get(username=username)
    if isinstance(date, str):
        created_at = parse_datetime(date)
        if created_at is None:
            raise ValueError("Invalid date string format")
    else:
        created_at = date

    order_kwargs = {"user": user}
    if created_at:
        order_kwargs["created_at"] = created_at

    order = Order.objects.create(**order_kwargs)

    for t in tickets:
        movie_session = MovieSession.objects.get(id=t["movie_session"])
        ticket = Ticket(
            movie_session=movie_session,
            order=order,
            row=t["row"],
            seat=t["seat"],
        )
        ticket.save()
    return order


def get_orders(
    username: str = None,
) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
