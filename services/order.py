from django.db.models import QuerySet
from django.db import transaction
from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> None:

    user_check = User.objects.get(username=username)
    order = Order.objects.create(user=user_check)
    if date is not None:
        order.created_at = date
        order.save()
    for ticket in tickets:
        session = MovieSession.objects.get(id=ticket.get("movie_session"))
        Ticket.objects.create(order=order,
                              movie_session=session,
                              row=ticket.get("row"),
                              seat=ticket.get("seat"))


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username).values_list()

    return Order.objects.all()
