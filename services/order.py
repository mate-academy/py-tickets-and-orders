from django.db import transaction

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets, username, date=None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            Ticket.objects.create(movie_session=movie_session,
                                  order=order,
                                  row=ticket["row"],
                                  seat=ticket["seat"])


def get_orders(username=None):
    orders = Order.objects.all().order_by("-id")
    if username:
        orders = orders.filter(user__username=username)
    return orders
