from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order | None:

    with (transaction.atomic()):
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist as e:
            raise ValidationError(str(e))

        order = Order.objects.create(user=user)

        if date and isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket in tickets:
            try:
                movie_sessions = (
                    MovieSession.objects.get(id=ticket["movie_session"])
                )
            except ObjectDoesNotExist as e:
                raise ValidationError(e)

            Ticket.objects.create(
                order=order,
                movie_session=movie_sessions,
                row=ticket["row"],
                seat=ticket["seat"],
            )

        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
