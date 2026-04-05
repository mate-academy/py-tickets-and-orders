from typing import Optional
from db.models import User, MovieSession, Order, Ticket
from django.db import transaction


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None,
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data.pop("movie_session"))
            ticket = Ticket(order=order,
                            movie_session=movie_session, **ticket_data)
            ticket.save()

        if date:
            order.created_at = date
            order.save()

        return order


def get_orders(username: Optional[str] = None) -> list[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
