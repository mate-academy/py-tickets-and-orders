from django.db import transaction
from db.models import Order, Ticket, User
from django.utils.dateparse import parse_datetime


def create_order(tickets, username, date=None):
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = parse_datetime(date)
            order.save()

        for t in tickets:
            Ticket.objects.create(
                movie_session_id=t["movie_session"],
                order=order,
                row=t["row"],
                seat=t["seat"]
            )

        return order


def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
