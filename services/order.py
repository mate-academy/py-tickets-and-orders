from django.db.models import QuerySet
from django.utils.datetime_safe import datetime

from db.models import Ticket, Order, User, MovieSession
from django.db import transaction


@transaction.atomic
def create_order(tickets: list[Ticket],
                 username: str,
                 date: str = None) -> QuerySet:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        movie_session = (MovieSession.objects
                         .get(id=ticket_data["movie_session"]))
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
