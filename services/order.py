from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


def create_order(tickets, username, date=None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(
            user=user,
        )

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket_data["movie_session"])
            ticket_data["movie_session"] = movie_session

            Ticket.objects.create(order=order, **ticket_data)


def get_orders(username=None):
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset.order_by('-id')
