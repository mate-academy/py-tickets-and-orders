from typing import Union
from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket, MovieSession

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Union[datetime, str] = None,
) -> Order:
    user = User.objects.get(username=username)

    if isinstance(date, str):
        try:
            created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError(
                f"Invalid date format: {date}. Expected '%Y-%m-%d %H:%M'."
            )
    elif isinstance(date, datetime):
        created_at = date
    elif date is None:
        created_at = None
    else:
        raise TypeError(
            f"Date must be str in format "
            f"'%Y-%m-%d %H:%M' or datetime, not {type(date)}"
        )
    order_data = {"user": user}
    if created_at is not None:
        order_data["created_at"] = created_at

    order = Order.objects.create(**order_data)
    if created_at:
        order.created_at = created_at
        order.save(update_fields=["created_at"])

    ticket_objs = []
    for ticket in tickets:
        movie_session = (MovieSession.objects
                         .get(id=ticket["movie_session"]))
        ticket_objs.append(
            Ticket(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie_session
            )
        )
    Ticket.objects.bulk_create(ticket_objs)
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    qs = (Order.objects.all()
          .prefetch_related("tickets", "tickets__movie_session"))
    if username:
        qs = qs.filter(user__username=username)
    return qs
