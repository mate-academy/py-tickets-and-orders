from django.db import transaction

from db.models import Ticket, Order, User, MovieSession


def create_order(tickets: list[dict],
                 username: str, date: str = None) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username),)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            tick = Ticket.objects.create(movie_session=MovieSession.
                                         objects.
                                         get(id=ticket["movie_session"]),
                                         order=order, row=ticket["row"],
                                         seat=ticket["seat"])
            tick.save()
    return order


def get_orders(username: str = None) -> User:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
