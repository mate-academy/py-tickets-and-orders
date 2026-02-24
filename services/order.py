from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth import get_user_model
import datetime

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> Order:
    user_model = get_user_model()

    user = user_model.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.created_at = parsed_date
        order.save(update_fields=["created_at"])

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(pk=ticket["movie_session"]),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
