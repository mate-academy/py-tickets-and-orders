from django.db import transaction
from datetime import datetime
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession
from typing import Optional, Union

User = get_user_model()


@transaction.atomic
def create_order(tickets: list, username: str,
                 date: Optional[Union[str, datetime]] = None) -> Order:
    user = User.objects.get(username=username)
    parsed_date = None
    if isinstance(date, str):
        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    elif isinstance(date, datetime):
        parsed_date = date

    order = Order.objects.create(user=user)

    # Se houver uma data, sobrescreve manualmente o campo created_at
    if parsed_date:
        order.created_at = parsed_date
        order.save(update_fields=["created_at"])

    for ticket in tickets:
        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=movie_session
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
