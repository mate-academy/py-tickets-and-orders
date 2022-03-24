from typing import List

from django.db import transaction

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: List[dict], username, date=None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
        order.save()

        for ticket_data in tickets:
            if ticket_data["movie_session"]:
                movie_session = MovieSession.objects.get(
                    pk=ticket_data["movie_session"])
                ticket_data["movie_session"] = movie_session

            Ticket.objects.create(order=order, **ticket_data)


def get_orders(username=None):
    order = Order.objects.all()
    if username:
        order = order.filter(user__username=username)
    return order
