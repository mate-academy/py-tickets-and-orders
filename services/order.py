import datetime

from django.db import transaction

from db.models import Order, User, Ticket


def create_order(tickets: list[dict], username: str, date: datetime = None):

    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(row=ticket["row"], seat=ticket["seat"],
                                  movie_session_id=ticket["movie_session"],
                                  order=order)
        return order


def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
