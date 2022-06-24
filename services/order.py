from django.db import transaction
from django.contrib.auth import get_user_model

from db.models import Ticket, Order


def create_order(tickets, username, date=None):
    with transaction.atomic():

        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            Ticket.objects.create(movie_session_id=ticket["movie_session"],
                                  row=ticket["row"],
                                  seat=ticket["seat"],
                                  order=order,
                                  )
        return order


def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
