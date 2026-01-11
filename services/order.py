from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list, username: str, date: str = None) -> Order:
    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError(f"User with username {username} not found.")
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            try:
                movie_session = MovieSession.objects.get(
                    id=ticket["movie_session"])
            except MovieSession.DoesNotExist:
                raise ValueError
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie_session,
                order=order)
        return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        return queryset.filter(user__username=username)
    return queryset
