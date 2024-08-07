from django.db import transaction
from django.utils import timezone
from db.models import Order, Ticket, MovieSession, User
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


def create_order(tickets: list, username: str, date=None):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return None


    with transaction.atomic():

        order = Order.objects.create(user=user)

        if date:

            order.created_at = timezone.make_aware(datetime.strptime(date, "%Y-%m-%d %H:%M"))
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(pk=ticket_data['movie_session']),
                order=order,
                row=ticket_data['row'],
                seat=ticket_data['seat']
            )
    return order


def get_orders(username=None):

     if username:
        return Order.objects.filter(user__username=username).order_by('-created_at')
     return Order.objects.all().order_by('-created_at')
