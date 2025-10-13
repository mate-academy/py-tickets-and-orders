from django.db import transaction
from django.utils.dateparse import parse_datetime
from db.models import Order, Ticket, User, MovieSession


def create_order(tickets, username, date=None):
    user = User.objects.get(username=username)
    with transaction.atomic():
        if date:
            order = Order.objects.create(user=user, created_at=parse_datetime(date))
        else:
            order = Order.objects.create(user=user)

        for t in tickets:
            movie_session = MovieSession.objects.get(id=t['movie_session'])
            ticket = Ticket(
                movie_session=movie_session,
                order=order,
                row=t['row'],
                seat=t['seat']
            )
            ticket.save()
    return order


def get_orders(username=None):
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
