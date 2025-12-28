from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import User, MovieSession, Ticket, Order


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
        order.save()

        for ticket_info in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket_info["movie_session"]
            )
            ticket = Ticket(
                row=ticket_info["row"],
                seat=ticket_info["seat"],
                movie_session=movie_session,
                order=order,
            )
            ticket.full_clean()
            ticket.save()

        return order


def get_orders(username: User = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
