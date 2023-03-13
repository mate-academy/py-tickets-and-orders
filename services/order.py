from db.models import Order, Ticket, User, MovieSession
from django.db import transaction


def create_order(tickets: list[dict], username, date=None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        for ticket in tickets:
            movie_session = MovieSession.objects.get(id=ticket["movie_session"])
            Ticket.objects.create(order=order, row=ticket["row"], seat=ticket["seat"], movie_session=movie_session)

        if date:
            order.created_at = date
            order.save()

        return order


def get_orders(username=None):
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders

