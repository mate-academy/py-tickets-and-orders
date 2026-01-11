import datetime

from django.db import transaction

from db.models import Order, User, MovieSession, Ticket


def create_order(tickets: list[dict], username: str, date: datetime = None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        if date:
            order = Order.objects.create(user=user, created_at=date)
        else:
            order = Order.objects.create(user=user)
        for item in tickets:
            movie_session = MovieSession.objects.get(id=item["movie_session"])
            Ticket.objects.create(movie_session=movie_session,
                                  seat=item["seat"],
                                  row=item["row"],
                                  order=order)
        order.save()
        return order

def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user__username__icontains=username)
    return Order.objects.all()

