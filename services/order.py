import distutils
from datetime import date
from db.models import Order
from django.db import transaction
from typing import List
from db.models import MovieSession, User, Ticket
from django.contrib.auth.models import User


@transaction.atomic
def create_order(tickets: List[dict], username, date=None):
    user, created = User.objects.get_or_create(username=username)
    order, created = Order.objects.get_or_create(user=user)
    if date is not None:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")
        movie_session = MovieSession.objects.get(pk=1)
        ticket, created = Ticket.objects.get_or_create(row=row, seat=seat, movie_session=movie_session, order=order)
        ticket.order = order
        ticket.save()
        # if date is not None:
        #     Order.objects.update_or_create(user=username, created_at=date)
        #     Ticket.objects.update_or_create(row=row, seat=seat, movie_session=movie_session)
        # else:
        #     Order.objects.update_or_create(user=username)
        #     Ticket.objects.update_or_create(row=row, seat=seat, movie_session=movie_session)
    #return


def get_orders(username=None):
    if username is not None:
        return Order.objects.filter(user__username=username).order_by("created_at")
    elif username is None:
        return Order.objects.all().order_by("-created_at")
